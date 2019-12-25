% ---------- Interface ----------
function Para = LPPL(Times, Prices, X0)
    % Pre-process
    N      = length(Times);
    Times  = transpose(Times(:));
    Prices = Prices(:);
    X0     = X0(1);
    % ------- TRAIN -------
    Para = Train(Times, Prices, X0);
    % ------- PREDICT -------
    Y    = Predict(Para, 1:N);
    % ------- FIGURE -------
    plot(Times, Prices, Times, Y);
    legend('exact', 'fitted');
end


% ---------- FUNCTIONS ----------
% ------- TRAIN -------
function Para = Train(Times, Prices, t0)
    %{
    Train function solve the optimization problem and get the optimal
    paramater.
    ----------------------------
    Args:
        Times:  Time sequence (suggested to be 1:N).
        Prices: Prices list.
        t0:     The start point for the optimization.
    Returns:
        Para:   Struct instance.
    %}
    ObjFunc      = @(t) Func2(t, Times, log(Prices));
    OptimProblem = createOptimProblem('fmincon',...
        'objective', ObjFunc,...
        'lb',        max(Times),...
        'x0',        t0,...
        'options',   optimset('Display', 'iter'));
    [tmin, Fmin] = fmincon(OptimProblem);
    
    [~, Para]  = Func2(tmin, Times, log(Prices));
    Para.tc    = tmin;
    Para.m     = Para.m;
    Para.omega = Para.omega;

    [~, tmp] = Func1(tmin, Para.m, Para.omega, Times, log(Prices));
    Para.A   = tmp.A;
    Para.B   = tmp.B;
    Para.C1  = tmp.C1;
    Para.C2  = tmp.C2;

    Para.TrainRes = Fmin;

    function [Value, Para] = Func2(t, Times, LogPrices)
        ObjSubFunc = @(x) Func1(t, x(1), x(2), Times, LogPrices);
        OptimSubProblem = createOptimProblem('fmincon',...
            'objective', ObjSubFunc,...
            'lb',        [0, 0],...
            'ub',        [1, Inf],...
            'x0',        [0.5, 2],...
            'options',   optimset('Display', 'off'));
        [Xmin, Value] = fmincon(OptimSubProblem);

        Para.m     = Xmin(1);
        Para.omega = Xmin(2);
    end

    function [Value, Para] = Func1(t, m, omega, Times, LogPrices)
        dt = t - Times;
        N  = length(dt);
        X  = zeros(N, 4);

        X(:,1) = 1.0;
        X(:,2) = dt .^ m;
        X(:,3) = X(:,2)' .* cos(omega*log(dt));
        X(:,4) = X(:,2)' .* sin(omega*log(dt));

        Coef    = regress(LogPrices, X);
        Para.A  = Coef(1);
        Para.B  = Coef(2);
        Para.C1 = Coef(3);
        Para.C2 = Coef(4);

        Value = sum((LogPrices - X*Coef).^2);
    end
end


% ------- PREDICT -------
function Y = Predict(Para, X)
    dt    = Para.tc - X;
    [M,N] = size(X);
    Y     = Para.A * ones(M,N) + Para.B * dt.^ Para.m + ...
            Para.C1 * dt .^ Para.m .* cos(Para.omega .* log(dt)) + ...
            Para.C2 * dt .^ Para.m .* sin(Para.omega .* log(dt));
    Y     = exp(Y);
end
