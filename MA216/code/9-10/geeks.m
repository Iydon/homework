function [C, Cdelta, Cvega, P, Pdelta, Pvega] = geeks(S,E,r,sigma,tau)
    %{
    :Argument:
        - S: [str, float], asset price @ time t
        - E: [str, float], exercise price
        - r: [str, float], interest rate
        - σ: [str, float], volatility
        - τ: [str, float], time to expiry (T-t)
        - to_simple: bool, wheather to simplify result
        - to_str: bool, wheather to convert result to str
        - to_latex: bool, wheather to convert result to latex

    :Output:
        - C, call value
        - Cδ, δ value of call
        - Cν, ν value of call
        - Cθ, θ value of call
        - Cρ, ρ value of call
        - Cγ, γ value of call
        - P, put value
        - Cδ, δ value of put
        - Cν, ν value of put
        - Cθ, θ value of put
        - Cρ, ρ value of put
        - Cγ, γ value of put

    :Example:
        >>> S=1.0; E=1.5; r=0.05; σ=0.2; τ=1.0;
        >>> greeks(S, E, r, σ, τ)
    %}
    if tau > 0
        d1 = (log(S/E) + (r + sigma^2/2)*tau) / (sigma*sqrt(tau));
        d2 = d1 - sigma*sqrt(tau);
        Nd1 = (1+erf(d1/sqrt(2))) / 2;
        Nd2 = (1+erf(d2/sqrt(2))) / 2;
        C = S*Nd1-E*exp(-r*(tau))*Nd2;
        Cdelta = Nd1;
        Cvega = S*sqrt(tau)*exp(-d1^2/2) / sqrt(2*pi);
        P = C + E*exp(-r*tau) - S;
        Pdelta = Cdelta - 1;
        Pvega = Cvega;
    else
        C = max(S-E, 0);
        Cdelta = (sign(S-E) + 1) / 2;
        Cvega = 0;
        P = max(E-S, 0);
        Pdelta = Cdelta - 1;
        Pvega = 0;
    end
end
