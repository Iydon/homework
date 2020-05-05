f = @(x, y) (12*x.^2-12*x+2).*y.^2.*(1-y).^2 + x.^2.*(1-x).^2.*(12*y.^2-12*y+2);
u = @(x, y) x.^2 .* y.^2 .* (1-x).^2 .* (1-y).^2;

Ns = 2.^(4:8) + 1;
errors = zeros(length(Ns), 2);

ith = 1;
for N = Ns
    h = 1 / (N+1);
    % five-point central finite difference method
    A = sparse( ...
        [1:N^2, 1:N^2-1, 2:N^2, N+1:N^2, 1:N^2-N], ...
        [1:N^2, 2:N^2, 1:N^2-1, 1:N^2-N, N+1:N^2], ...
        [-4*ones(1, N^2), ones(1, 4*N^2-2*N-2)]/h^2 ...
    );
    [X, Y] = meshgrid(linspace(0, 1, N));
    F = reshape(f(X, Y), N^2, 1);

    % data
    U0 = u(X, Y);  % solution
    U1 = reshape(internal_solver(A, F), N, N);  % A \ b
    U2 = reshape(sor_solver(A, F), N, N);  % SOR
    U3 = reshape(dst_solver(A, F, true), N, N);  % DST

    % figure
    figure
    jth = 1;
    for U = {U0, U1, U2, U3}
        subplot(2, 2, jth)
        surf(U{1})
        shading interp
        jth = jth + 1;
    end

    % errors
    [L2, Linf] = compute_errors(U0, U1);
    errors(ith, :) = [L2; Linf];
    ith = ith + 1;
end

% errors
figure
loglog(1./(Ns+1), errors)
legend('L2', 'Linf')



function X = internal_solver(A, F)
    %{
    MATLAB mldivide.
    %}
    X = A \ F;
end


function X = dst_solver(A, F, lambda)
    if nargin < 3 || ~lambda
        lambda = eig(A);
    else
        N = sqrt(length(F));
        h = 1 / (N+1);
        [p, q] = meshgrid(1: N);
        lambda = 2/h^2 * (cos(p*pi*h)+cos(q*pi*h)-2);
        lambda = reshape(lambda', N^2, 1);
    end
    X = dst2(idst2(F) ./ lambda);
end


function X = sor_solver(A, F, maxiter, X0, omega, epsilon)
    %{
    SOR iteration method.

    Argument:
        - A: matrix
        - F: column vector
        - maxiter: int, max iteration number
        - X0: column vector, initial value of X
        - omega: float, relaxation parameter
        - epsilon: expected accuracy

    Return:
        - X: matrix, A*X=F
    %}
    if nargin<6, epsilon = 1e-6; end
    if nargin<5, omega=2./(1+sin(pi/sqrt(length(F)))); end
    if nargin<4, X0=rand(length(F), 1); end
    if nargin<3, maxiter=2048; end

    D = diag(diag(A));
    L = tril(A) - D;
    U = triu(A) - D;

    for i = 1: maxiter
        X = (D+omega*L) \ (((1-omega)*D-omega*U)*X0 + F);
        if norm(X-X0) < epsilon
            fprintf('[+] %d step(s) -> accuracy %.3e\n', i, epsilon);
            return;
        end
        X0 = X;
    end
    fprintf('[-] Not convergence\n');
end


function [L2, Linf] = compute_errors(y_true, y_pred)
    delta = y_true - y_pred;
    L2 = norm(delta, 2);
    Linf = norm(delta, inf);
end
