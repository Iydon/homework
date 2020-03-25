warning off;
when_to_adult = 20;
data = [0,10; 1,35; when_to_adult,7500];
x = data(:, 1);
y = data(:, 2);

%% Brody
ft = fittype( 'exp1' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = [0 0];
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Brody-1'); %#ok

ft = fittype({'1', '(exp(-x))'}, 'independent', 'x', 'dependent', 'y', 'coefficients', {'a', 'b'});
opts = fitoptions;
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Brody-2'); %#ok


%% Logistic
ft = fittype('a/(1+b*exp(-x))', 'independent', 'x', 'dependent', 'y');
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = rand(1, 2);
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Logistic'); %#ok


%% Bertalanffy
ft = fittype( '[a/b-(a/b-10^(1/3))*exp(-b*x/3)]^3', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = rand(1, 2);
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Bertalanffy'); %#ok


%% Gompertz
ft = fittype( 'a*exp(-exp(b-c*x))', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = rand(1, 3);
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Gompertz'); %#ok


%% Richards
ft = fittype( 'a*(1-b*exp(-x))^c', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Display = 'Off';
opts.StartPoint = rand(1, 3);
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Richards'); %#ok


%% Janoschek
ft = fittype( 'a-(a-10)*exp(-b*x)', 'independent', 'x', 'dependent', 'y' );
opts = fitoptions( 'Method', 'NonlinearLeastSquares' );
opts.Algorithm = 'Levenberg-Marquardt';
opts.Display = 'Off';
opts.StartPoint = rand(1, 2);
[fitresult, gof] = fit_plot(x, y, ft, opts, 'Janoschek');



%% Fit function
function [fitresult, gof] = fit_plot(x, y, ft, opts, name)
%  Args:
%      X Input : x
%      Y Output: y
%  Output:
%      fitresult : a fit object representing the fit.
%      gof : structure with goodness-of fit info.
    try
        [fitresult, gof] = fit(x, y, ft, opts);
        model = struct(fitresult);
        % model.defn and model.coeffValues
        disp([name, '    RMSE: ', num2str(gof.rmse), ...
                    '    R^2: ', num2str(gof.rsquare)]);
        figure('Name', name);
        hold on;
        loglog(x, y, 'o');
        xx = linspace(0, 100, 128);
        loglog(xx, fitresult(xx));
        legend('Y vs. X', name, 'Location', "NorthEast");
        text(50, 3000, ['R^2: ', num2str(gof.rsquare)])
        title([name, ': ', model.defn]);
        xlabel Time(Year)
        ylabel Weight(kg)
        grid on;
        saveas(gcf,name,'epsc')
    catch
        disp([name, ' Failed']);
        fitresult = NaN;
        gof = NaN;
    end
end