#!/usr/bin/python3
import sympy


def deriving_finite_difference_approximations(u, x, h, hs, order=1, errors=1):
    '''See also `1_2.py`.
    '''
    # the method of undetermined coefficients
    length = len(hs)
    hs = sympy.Matrix([hs])
    _hs = sympy.ones(1, length)
    A = sympy.ones(length)
    for ith in range(1, length):
        _hs = _hs.multiply_elementwise(hs)
        A[ith, :] = _hs
    b = sympy.zeros(length, 1)
    b[order] = sympy.factorial(order)
    coefficients = A.solve(b)
    # errors
    _errors = [None] * errors
    Du = u(x).diff(x, length-1)
    denominator = sympy.factorial(length-1)
    for ith in range(errors):
        denominator *= length + ith
        _hs = _hs.multiply_elementwise(hs)
        coefficient = coefficients.dot(_hs) / denominator
        Du = Du.diff()
        _errors[ith] = coefficient * h**(length+ith-order) * Du
    # finite difference approximations
    Du = sum(c*u(x+a*h) for c, a in zip(coefficients, hs))
    return Du/h**order, sum(_errors)


if __name__ == '__main__':
    u = sympy.Function('u')
    x, h = sympy.symbols('x, h')

    hs = [0, -1, -2]
    order = 1
    D1u, errors = deriving_finite_difference_approximations(u, x, h, hs, order, 1)
    sympy.pretty_print(D1u + errors)

    hs = [-1, 0, 1]
    order = 2
    D2u, errors = deriving_finite_difference_approximations(u, x, h, hs, order, 2)
    sympy.pretty_print(D2u + errors)
