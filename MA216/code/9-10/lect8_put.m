% Evaluation
E = 1;
r = 0.05;
sigma = 0.2;
T = 1;
L = 50;

Svals = linspace(0, 3, L);
tvals = linspace(0, T, L);
P = zeros(L);
for n = 1 : L*L
    i = floor((n-1)/L) + 1;
    j = mod((n-1), L) + 1;
    [~, ~, Put, ~] = bs_price(Svals(i), E, r, sigma, T-tvals(j));
    P(i, j) = Put;
end

% Figure
figure;
hold on;

[Smat, tmat] = meshgrid(Svals, tvals);
mesh(Smat, tmat ,P')
ylabel('t');
xlabel('S');
zlabel('P(S,t)');

% Evaluation
S = 1.1;
mu = r;
L = 1e4;
dt = T / L;
M = 1;
tvals = 0: dt: T;

Svals = S * cumprod( ...
        exp((mu-sigma^2/2)*dt + ...
        sigma*(dt)^(1/2)*randn(M, L)), ...
    2);
Svals = [S*ones(M, 1), Svals];

P1 = zeros(size(tvals));
for i = 1 : length(tvals)
        [~, ~, Put, ~] = bs_price(S, E, r, sigma, T-tvals(i));
        P1(i) = Put;
end

% Figure
plot3(Svals, tvals, zeros(size(tvals)));
plot3(Svals, tvals, P1);
alpha(0.5);
