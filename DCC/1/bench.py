#!/usr/bin/python3
import sys
sys.path.append('../0')

import matplotlib.pyplot as plt

from model import Denoising


I = plt.imread('demo.png')[:, :, 0]
d = Denoising(I)
J = d.apply('TV')

plt.imsave('bench.png', J, cmap=plt.cm.gray)
