#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : 8-a.py
@Time      : 2019/11/14
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from os import get_terminal_size
columns = get_terminal_size().columns

from sympy import symbols, integrate, diff, exp, sqrt, log
from sympy import oo, pi as π
from sympy import pretty_print
hw7a = __import__('7-a')


# Symbols
S, E, r, σ, T, t = (getattr(hw7a, _) for _ in ('S', 'E', 'r', 'σ', 'T', 't'))
d1, d2 = hw7a.d1, hw7a.d2
_ = symbols('_')

N:_ = integrate(exp(-_**2/2)/(sqrt(2*π)), (_, -oo, _))
dN:_ = diff(N, _)



if __name__ == "__main__":
    # Results in Different Format
    ZERO = S*dN.subs(_, d1) - exp(-r*(T-t))*E*dN.subs(_, d2)
    ONE = (S*dN.subs(_, d1)) / (exp(-r*(T-t))*E*dN.subs(_, d2))

    # Simplify Result
    print(f'{" ZERO ":=^{columns}}')
    pretty_print(ZERO.simplify(), use_unicode=False)

    print()

    print(f'{" ONE ":=^{columns}}')
    pretty_print(ONE.simplify(), use_unicode=False)
