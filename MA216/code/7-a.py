from sympy import symbols, log, sqrt, pretty_print


S, E, r, σ, T, t = symbols('S, E, r, σ, T, t')

numerator_l = log(S/E) + r*(T-t)
numerator_r = σ**2*(T-t)/2
denominator = σ*sqrt(T-t)

d1 = (numerator_l + numerator_r) / denominator
d2 = (numerator_l - numerator_r) / denominator

# Process:
__Δ = d1 - d2
#   = 2*numerator_r / denominator
#   = σ**2*(T-t) / σ*sqrt(T-t)
#   = σ * sqrt(T-t)
#   =     _______
#     σ⋅╲╱ T - t



if __name__ == "__main__":
    pretty_print(__Δ.simplify())
