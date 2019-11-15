#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : 8-b_MATLAB.py
@Time      : 2019/11/15
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from math import pi as π

import matlab
import matlab.engine
if 'engine' not in locals():
    engine = matlab.engine.start_matlab()


def greeks(S, E, r, σ, τ, to_simple=False, to_str=False, to_latex=False):
    '''Greeks.

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
    '''
    _f = lambda x: engine.str2sym(str(x))
    S, E, r, σ, τ = _f(S), _f(E), _f(r), _f(σ), _f(τ)
    乘方 = engine.power
    逆 = engine.inv
    乘 = engine.times
    除 = lambda x, y: 乘(x, 逆(y))
    加 = engine.plus
    减 = lambda x, y: 加(x, 乘(y, -1.))
    log, sqrt, erf, exp = engine.log, engine.sqrt, engine.erf, engine.exp
    d1 = 除(加(log(除(S, E)), 乘(加(r, 乘(1/2, 乘方(σ, 2))), τ)), 乘(σ, sqrt(τ)))
    d2 = 减(d1, 乘(σ, sqrt(τ)))
    Nd1 = 乘(1/2, 加(1, erf(除(d1, sqrt(2.)))))
    Nd2 = 乘(1/2, 加(1, erf(除(d2, sqrt(2.)))))
    Np1 = 除(exp(乘(-1/2, 乘方(d1, 2))), sqrt(乘(2., π)))

    C = 减(乘(S, Nd1), 乘(乘(E, Nd2), exp(乘(减(0, r), τ))))
    Cδ = Nd1
    Cν = 乘(乘(S, Np1), sqrt(τ))
    Cθ = 减(除(乘(乘(减(0, S), σ), Np1), 乘(2., sqrt(τ))),
        乘(乘(乘(r, E), Nd2), exp(乘(减(0, r), τ))))
    Cρ = 乘(乘(乘(E, τ), Nd2), exp(乘(减(0, r), τ)))
    Cγ = 除(Np1, 乘(乘(S, σ), sqrt(τ)))

    P = 加(减(C, S), 乘(E, exp(乘(减(0, r), τ))))
    Pδ = 减(Cδ, -1.)
    Pν = Cν
    Pθ = 加(除(乘(乘(减(0, S), σ), Np1), 乘(2., sqrt(τ))),
        乘(乘(乘(r, E), Nd2), exp(乘(减(0, r), τ))))
    Pρ = 减(Cρ, -1.)
    Pγ = Cγ

    result = C, Cδ, Cν, Cθ, Cρ, Cγ, P, Cδ, Cν, Cθ, Cρ, Cγ
    if to_simple:
        result = tuple(engine.simplify(r) for r in result)
    if to_str and not to_latex:
        result = tuple(engine.char(r) for r in result)
    if to_latex:
        result = tuple(engine.latex(r) for r in result)
    return result


if __name__ == "__main__":
    S='S'; E='E'; r='r'; σ='sigma'; τ='tau';
    result = greeks(S, E, r, σ, τ, to_simple=True, to_latex=True)
