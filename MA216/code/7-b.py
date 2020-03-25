from math import log, sqrt, erf, exp


S, E, r, σ, T, t = 5, 4, 0.05, 0.3, 1, 0

numerator_l = log(S/E) + r*(T-t)
numerator_r = σ**2*(T-t)/2
denominator = σ*sqrt(T-t)

d1 = (numerator_l + numerator_r) / denominator
d2 = (numerator_l - numerator_r) / denominator

N = lambda d: (1+erf(d/sqrt(2)))/2

print('    d₁ =', d1)
print('    d₂ =', d2)
print(' N(d₁) =', N(d1))
print(' N(d₂) =', N(d2))
print('N(-d₁) =', N(-d1))
print('N(-d₂) =', N(-d2))


C = S*N(d1) - E*exp(-r*(T-t))*N(d2)
P = E*exp(-r*(T-t))*N(-d2) - S*N(-d1)

print('              P+S =', P+S)
print('C+E*exp(-r*(T-t)) =', C+E*exp(-r*(T-t)))
