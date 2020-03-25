#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : quadratic_equation.py
@Author    : Iydon Liang
@Docstring : Solve the quadratic equation.
@Require   : Python==3.7.6; sympy==1.4
@Result    : \\
Poly(C2*x**2 + C1*x + C0, x, domain='ZZ[C0,C1,C2]')
            ________________
           /              2
   C1    \/  -4*C0*C2 + C1
- ---- - -------------------
  2*C2           2*C2
            ________________
           /              2
   C1    \/  -4*C0*C2 + C1
- ---- + -------------------
  2*C2           2*C2
'''
from sympy import symbols, Poly, roots, pretty_print
from sympy.assumptions import assuming, Q

# variables declaration
degree = 2
C = symbols(f'C0:{degree+1}')  # C_0, C_1, ..., C_degree
x = symbols('x')               # x^0, x^1, ..., x^degree
# calculate roots
with assuming(Q.nonzero(C[-1]), *map(Q.complex, C[:-1])):
    quadratic_equation = Poly(reversed(C), x)
    solutions = roots(quadratic_equation)
# display results
pretty_print(quadratic_equation, use_unicode=False)
for solution in solutions:
    pretty_print(solution, use_unicode=False)
