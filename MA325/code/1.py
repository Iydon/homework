#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : 1.py
@Time      : 2019/11/02
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : u_t-a^2u_{xx}=0, x\in (0, l), t>0
             u(0, t)=u(l, t)=0, t>0
             u(x, 0)=\phi (x), x\in [0, l]
'''

import numpy as np
from matplotlib import pyplot


a, l = 1, 1
ϕ = lambda x: (1/4<x).astype(float) * (x<3/4).astype(float)
ϕ = lambda x: np.abs(np.sin(2*np.pi*x))

nx = 50
nt = 100

dx = l / (nx-1)
dt = dx**2 / nt
u = ϕ(np.linspace(0, l, nx))
M = u.max()
def transform(u, nt, display=False):
    un = u.copy()
    k = a**2 * dt / dx**2
    if display: print(k)
    for n in range(nt+1):
        un[1:-1] = un[1:-1] + k*(un[2:]+un[:-2]-2*un[1:-1])
        un[0] = un[-1] = 0
    return un

up = transform(u, nt)
for i in range(128):
    pyplot.plot(up)
    pyplot.ylim([0, M])
    up = transform(up, nt)
    pyplot.pause(0.1)
    pyplot.cla()
