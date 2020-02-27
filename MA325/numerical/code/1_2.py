#!/usr/bin/python3
import numpy as np


def deriving_finite_difference_approximations(hs, order=1, errors=1):
    '''Deriving finite difference approximations
    using the method of undetermined coefficients.

    Example
        >>> # Du(x) = au(x) + bu(x-h) + cu(x-2h)
        >>> hs = [0, -1, -2]
        >>> order = 1
        >>> deriving_finite_difference_approximations(hs, order)
        ([1.5, -2.0, 0.5], [-0.3333333333333333])
        >>> # a, b, c = (1.5, -2.0, 0.5) / h^order
        >>> # Du(x)-u'(x) = -0.333 * h^2 * u^(3)(x)
        >>> # h^2: 2 = len(hs) + ith - order where errors[ith]=-0.333
    '''
    # the method of undetermined coefficients
    length = len(hs)
    _hs = np.ones(length)
    A = np.ndarray((length, length))
    A[0, :] = 1
    for ith in range(1, length):
        _hs *= hs
        A[ith, :] = _hs
    b = np.zeros(length)
    b[order] = np.math.factorial(order)
    coefficients = np.linalg.solve(A, b)
    # errors
    _errors = [None] * errors
    denominator = np.math.factorial(length-1)
    for ith in range(errors):
        denominator *= length + ith
        _hs *= hs
        _errors[ith] = sum(coefficients*_hs) / denominator
    return coefficients.tolist(), _errors


if __name__ == '__main__':
    hs = [0, -1, -2]
    order = 1
    c, e = deriving_finite_difference_approximations(hs, order, 3)
    print(c, e)

    hs = [-1, 0, 1]
    order = 2
    c, e = deriving_finite_difference_approximations(hs, order, 3)
    print(c, e)
