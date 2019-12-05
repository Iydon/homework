#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sympy import symbols
from sympy import integrate, diff, log, sqrt, exp, erf
from sympy import oo, pi as π


# In[2]:


class Simplify:
    _SIMPLIFY = 'simplify'

    def __init__(self, lazy=False):
        self._lazy = lazy

    def __call__(self, value, **kwargs):
        if self._lazy:
            return value
        _simplify = getattr(value, self._SIMPLIFY, None)
        if _simplify is not None:
            try:
                return _simplify(**kwargs)
            finally:
                print('Formula simplified.')

    def __ror__(self, value):
        return self.__call__(value)

simplify = Simplify(lazy=False)


# In[3]:


S, E, r, σ, T, t = symbols('S, E, r, σ, T, t')
_ = symbols('_')

d1 = (log(S/E) + r*(T-t) + σ**2*(T-t)/2) / (σ*sqrt(T-t))
d2 = d1 - σ*sqrt(T-t)

N = lambda x: (erf(sqrt(2)*x/2)+1)/2


C = S*N(d1) - E*exp(-r*(T-t)*N(d2)) | simplify
Δ = diff(C, S)
ν = diff(C, σ)
θ = diff(C, t)
γ = diff(C, S, 2)
