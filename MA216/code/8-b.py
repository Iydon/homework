#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : 8-b.py
@Time      : 2019/11/14
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from sympy import diff, exp
hw8a = __import__('8-a')


# Util
class Simplify:
    _SIMPLIFY = 'simplify'
    def __init__(self, lazy=False):
        self._lazy = lazy
    def __ror__(self, value):
        if self._lazy:
            return value
        _simplify = getattr(value, self._SIMPLIFY, None)
        if _simplify is not None:
            try:
                return _simplify()
            finally:
                print('Formula simplified.')
simplify = Simplify(lazy=False)

# Symbols
S, E, r, σ, T, t, d1, d2, _, N = (getattr(hw8a, _)
    for _ in ('S', 'E', 'r', 'σ', 'T', 't', 'd1', 'd2', '_', 'N'))


if __name__ == "__main__":
    # Derivation
    C = S*N.subs(_, d1) - E*exp(-r*(T-t)*N.subs(_, d2)) | simplify
    Δ = diff(C, S) | simplify
    Cₜ = diff(C, t) | simplify
    Γ = diff(C, S, 2) | simplify

    PDE = Cₜ + r*S*Δ + σ**2*S**2*Γ/2 - r*C | simplify
