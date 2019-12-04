function [C, Cdelta, P, Pdelta] = bs_price(S, E, r, sigma, tau)
    %{
        Argument
        --------
        S: asset price at time `t`
        E: exercise price
        r: interest rate
        sigma: volatility
        tau: time to expiry `T-t`

        Return
        ------
        C: call value
        Cdelta: delta value of call
        P: put value
        Pdelta: delta value of put

        Example
        -------
        >>> [C, Cdelta, P, Pdelta] = bs_price(5, 4, 0.05, 0.3, 1)
    %}
    if tau > 0
        d1 = (log(S/E) + (r+sigma^2/2)*tau) / (sigma*sqrt(tau)); 
        d2 = d1 - sigma*sqrt(tau);
        Nd1 = (1 + erf(d1/sqrt(2))) / 2;
        Nd2 = (1 + erf(d2/sqrt(2))) / 2;
        C = S*Nd1 - E*exp(-r*tau)*Nd2;
        Cdelta = Nd1;
        P = C + E*exp(-r*tau) - S;
        Pdelta = Cdelta - 1;
    else
        C = max(S-E, 0);
        Cdelta = (sign(S-E)+1) / 2;
        P = max(E-S, 0);
        Pdelta = Cdelta - 1;
    end
end
