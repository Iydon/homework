% Evaluation
r = 0.03;
S = 2;
E = 2;
T = 3;
tau = T;
sigma_true = 0.3;
[C_true, ~, P_true, ~] = bs_price(S, E, r, sigma_true, tau);

%% Newton's method
tol = 1e-8;
sigma = sqrt(2*abs((log(S/E)+r*T)/T));
sigmadiff = 1;
k = 1;
kmax = 100;
while sigmadiff>=tol && k<kmax
    [~, ~, ~, P, ~, Pvega] = geeks(S,E,r,sigma,tau);
    increment = (P-P_true) / Pvega;
    sigma = sigma - increment;
    k = k + 1;
    sigmadiff = abs(increment);
end

%% Black-Scholes implied volatility
disp("Implied volatility: " + blsimpv(S, E, r, tau, P_true));

% Evaluation
M = 100;
S = 3;
E = 1;
r = 0.05;
tau = 3;
sigma = linspace(0, 1.5, M);
[~, Pvalve] = blsprice(S, E, r, tau, sigma);
Pvega = zeros(M, 1);
for i = 1 : M
    Pvega(i) = blsvega(S, E, r, tau,sigma(i));
end

% Figure
figure;
subplot(2, 1, 1)
plot(sigma, Pvalve)
xlabel('\sigma');
ylabel('P(\sigma)')
subplot(2, 1, 2)
plot(sigma, Pvega)
xlabel('\sigma')
ylabel('\partial P/\partial \sigma')
