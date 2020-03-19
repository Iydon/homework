#!/usr/bin/python3
import sys
sys.path.append('../0')

import matplotlib.pyplot as plt
import numpy as np
from mpi4py import MPI

from model import Denoising


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
assert size==4

comm.Barrier()
tick = MPI.Wtime()

if rank == 0:
    I = plt.imread('demo.png')[:, :, 0]
    height, width = I.shape
    data = [
        I[height//2:, :width//2].flatten(),
        I[:height//2, width//2:].flatten(),
        I[height//2:, width//2:].flatten(),
    ]
else:
    height, width = 0, 0
height, width = comm.bcast((height, width), root=0)
if rank == 0:
    I = I[:height//2, :width//2]
    for i in range(1, size):
        comm.Send([data[i-1], MPI.FLOAT], dest=i, tag=10+i)
else:
    I = np.empty((1, height*width//4), dtype='f')
    comm.Recv([I, MPI.FLOAT], source=0, tag=10+rank)
    I = I.reshape((height//2, width//2))
d = Denoising(I)
J = d.apply('TV')
Is = None
if rank == 0:
    Is = np.empty([4, height*width//4], dtype='float64')
comm.Gather(J.flatten(), Is, root=0)
if rank == 0:
    result = np.empty((height, width))
    result[:height//2, :width//2] = Is[0].reshape((height//2, width//2))
    result[height//2:, :width//2] = Is[1].reshape((height//2, width//2))
    result[:height//2, width//2:] = Is[2].reshape((height//2, width//2))
    result[height//2:, width//2:] = Is[3].reshape((height//2, width//2))
    plt.imsave('comparsion.png', result, cmap=plt.cm.gray)

comm.Barrier()
elapsed_time = MPI.Wtime() - tick
print(elapsed_time)
