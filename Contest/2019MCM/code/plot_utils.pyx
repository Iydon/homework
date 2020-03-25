# -*- coding: utf-8 -*-
# @Time     : 2019/01/26 18:10
# @Author   : Iydon
# @File     : plot_utils.pyx
# @Compiler : Cython

import matplotlib.pyplot as plt


cdef public plot(x, y, name):
    plt.plot(x, y)
    plt.savefig(name)

cdef public loglog(x, y, name):
    plt.loglog(x, y)
    plt.savefig(name)