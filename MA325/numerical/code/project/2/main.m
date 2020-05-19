%{
Let u(i, j, n) := u_{i, j}^n and f(u) := u - u^3
Then
(1/∆t+β)*u(i, j, n+1) - ε/h^2*(u(i-1, j, n+1)+u(i+1, j, n+1)+u(i, j-1, n+1)+u(i, j+1, n+1)-4*u(i, j, n+1)) = (1/∆t+β)*u(i, j, n) + f(u(i, j, n))

Reference: https://arxiv.org/pdf/1906.06584.pdf
%}

% Parameters of Allen–Cahn equation
N = 255;
h = 2*pi / (N+1);
dt = 0.01;
epsilon = 0.1;
beta = 2;
f = @(U) U - U.^3;
U0 = get_U0(N);
A = get_A(N, dt, h, epsilon, beta);
% Parameters of others
number = ceil(50 / dt) + 1;
verbose = true;
gif_flag = false;
gif_delay = 0.01;
gif_filename = 'allen_cahn.gif';
solution_flag = true;
solution_height = 3;
solution_width = 2;
solutions_Ts = [0, 2, 5, 8, 20, 50];
energy = NaN(1, number);
% fast solver
[p, q] = meshgrid(1: N);
lambda = 1 + beta*dt - 2*(cos(p*h/2)+cos(q*h/2)-2)*epsilon^2*dt/h^2;

% Solve linear system
for ith = 1: number
    if verbose
        fprintf('[%d/%d]\n', ith, number);
    end
    % plot
    if gif_flag
        imagesc(to_2D(U0, N));
        axis off;
        colorbar;
        title(num2str(ith));
        to_gif(frame2im(getframe(gcf)), gif_filename, gif_delay, ith);
    end
    if solution_flag
        for jth = 1: length(solutions_Ts)
            if (ith-1)*dt == solutions_Ts(jth)
                to_subplot(U0, N, jth, solution_height, solution_width, solutions_Ts(jth));
            end
        end
    end
    % iterate
    energy(ith) = get_energy(U0, N, epsilon, h);
    tic;
    F = get_F(U0, dt, beta, f);
    % U0 = matlab_solver(A, F);
    U0 = dst_solver(lambda, F, U0, N, f, beta, dt);
    toc
end
% plot((1: number)*dt, energy)



function U0 = matlab_solver(A, F)
    U0 = A \ F;
end

function U0 = dst_solver(lambda, F, U0, N, f, beta, dt)
    F = f(U0)*dt + (1+beta*dt)*U0;
    U0 = dst2(idst2(reshape(F, N, N)) ./ lambda);
end

function U0 = get_U0(N)
    % U0 has zero mean with size (N, N)
    U0 = 0.05 * (2*rand(N^2, 1) - 1);
    U0 = U0 - mean(U0);
end

function A = get_A(N, dt, h, epsilon, beta)
    % A*U = F
    A = sparse( ...
        [1: N^2, 1: N^2-1, 2: N^2, N+1: N^2, 1: N^2-N], ...
        [1: N^2, 2: N^2, 1: N^2-1, 1: N^2-N, N+1: N^2], ...
        [(1/dt+beta+4*epsilon^2/h^2)*ones(1, N^2), -epsilon^2/h^2*ones(1, 4*N^2-2*N-2)] ...
    );
end

function F = get_F(U, dt, beta, f)
    % A*U = F
    F = (1/dt+beta)*U + f(U);
end

function E = get_energy(U, N, epsilon, h)
    U = reshape(U, N, N);
    kernel = (U.^2-1).^2/4 - epsilon^2/2*U.*gradient(U);
    E = sum(sum(h^2*kernel));
end

function M = to_2D(U, N)
    M = reshape(U, N, N);
end

function to_gif(RGB, filename, delay, ith)
    % Argument:
    %   - RGB: 3-D matrix
    %   - filename: chars
    %   - delay: double
    %
    % Example:
    %   >> to_gif(frame2im(getframe(gcf)), 'target.gif', 0.5, 1);
    [I, map] = rgb2ind(RGB, 20);
    if ith == 1
        imwrite(I, map, filename, 'gif', 'Loopcount', inf, 'DelayTime', delay);
    else
        imwrite(I, map, filename, 'gif', 'WriteMode', 'append', 'DelayTime', delay);
    end
end

function to_subplot(U, N, ith, height, width, T)
    subplot(height, width, ith);
    imagesc(to_2D(U, N));
    axis off;
    title(['T = ', num2str(T)]);
end
