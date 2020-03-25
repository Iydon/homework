#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : trajectory.py
@Time      : 2019/12/15
@Author    : Iydon Liang
@Contact   : liangiydon AT gmail.com
@Docstring : Draw the picture of trajectories.
@Require   : Python==3.7.6; matplotlib==3.1.2;numpy==1.17.4
@Result    : <pictures>
'''
import numpy as np
import matplotlib.pyplot as plt


θs = 15, 30, 45, 60, 75
V = g = 9.8

Sx = np.linspace(0, 2*V**2/g, 128)
for θ in np.deg2rad(θs):
    Sy = Sx * (np.tan(θ) - g*Sx/(2*(V*np.cos(θ))**2))
    Sy[np.sum(Sy>=0.)+1:] = np.nan
    plt.plot(Sx, Sy)
    idx = np.sum(Sx < .1*V**2/g*np.sin(2*θ))
    plt.arrow(Sx[idx], Sy[idx],
        Sx[idx+1]-Sx[idx], Sy[idx+1]-Sy[idx],
        head_width=.1, overhang=1)

plt.legend([f'{θ}°' for θ in θs])
plt.text(0, 0, 'O', fontsize=12,
    horizontalalignment='right', verticalalignment='top')
plt.grid()
plt.xlabel('Range')
plt.ylabel('Height')
plt.show()
