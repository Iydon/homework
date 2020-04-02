#!/usr/bin/python3
'''
@Reference: https://github.com/wenj18/HW_TV3d
'''
import collections
import numpy as np


class Worker:
    '''
    '''
    def __init__(self, I, dt=1e-1, lam=1e-2, eps=1e-4):
        '''
        '''
        self.I = I
        self._dt = dt
        self._lam = lam
        self._eps = eps
        self._size = I.shape

    def next(self, J, number=8):
        row, col, channel = self._size
        for ith in range(number):
            start = ith*row // number - 1
            end = (ith+1)*row // number + 1
            if start < 0:
                start += 1
                DfJx = J[(start+1):(end+1), :, :] - J[start:end, :, :]
            elif end > row:
                end -= 1
                DfJx = J[list(range(start+1, end))+[end-1], :, :] - J[start:end, :, :]
            else:
                DfJx = J[(start+1):(end+1), :, :] - J[start:end, :, :]
            DfJy = J[start:end, list(range(1, col))+[col-1], :] - J[start:end, :, :]
            DfJz = J[start:end, :, list(range(1, channel))+[channel-1]] - J[start:end, :, :]
            TempDJ = (self._eps + DfJx*DfJx + DfJy*DfJy + DfJz*DfJz) ** (1/2)
            DivJx = DfJx / TempDJ
            DivJy = DfJy / TempDJ
            DivJz = DfJz / TempDJ
            mi, ni, li = DivJx.shape
            if start == 0:
                div = DivJx[0:(mi-1), :, :] - DivJx[[0]+list(range(mi-2)), :, :] \
                    + DivJy[0:(mi-1), :, :] - DivJy[0:(mi-1), [0]+list(range(ni-1)), :] \
                    + DivJz[0:(mi-1), :, :] - DivJz[0:(mi-1), :, [0]+list(range(li-1))]
                J[start:(end-1), :, :] += self._dt*div \
                    - self._dt * self._lam * (J[start:(end-1), :, :]-self.I[start:(end-1), :, :])
            elif end == row:
                mi += 1
                end += 1
                div = DivJx[1:(mi-1), :, :] - DivJx[0:(mi-2), :, :] \
                    + DivJy[1:(mi-1), :, :] - DivJy[1:(mi-1), [0]+list(range(ni-1)), :] \
                    + DivJz[1:(mi-1), :, :] - DivJz[1:(mi-1), :, [0]+list(range(li-1))]
                J[(start+1):(end-1), :, :] += self._dt*div \
                    - self._dt * self._lam * (J[(start+1):(end-1), :, :]-self.I[(start+1):(end-1), :, :])
            else:
                div = DivJx[1:(mi-1), :, :] - DivJx[0:(mi-2), :, :] \
                    + DivJy[1:(mi-1), :, :] - DivJy[1:(mi-1), [0]+list(range(ni-1)), :]\
                    + DivJz[1:(mi-1), :, :] - DivJz[1:(mi-1), :, [0]+list(range(li-1))]
                J[(start+1):(end-1), :, :] += self._dt*div \
                    - self._dt * self._lam * (J[(start+1):(end-1), :, :]-self.I[(start+1):(end-1), :, :])
        return J

    @classmethod
    def split(cls, total, number):
        total = tuple(total)
        length = len(total)
        start = 0
        for ith in range(number):
            end = (ith+1) * length // number
            yield total[start:end]
            start = end

    @classmethod
    def split_images(cls, Is, number):
        *_, total = Is.shape
        for idx in cls.split(range(total), number):
            yield Is[:, :, idx]


def default_image(nx=200, ny=200, nz=200, mean=0, sigma=12):
    I = 100 * np.ones((nx, ny, nz), dtype='float64')
    f = lambda ratio1, ratio2, number: slice(int(number*ratio1), int(number*ratio2))
    I[f(0.5, 0.75, nx), f(0.5, 0.75, ny), f(0.5, 0.75, nz)] = 150.0
    return I + np.random.normal(mean, sigma, (nx, ny, nz))


if __name__ == '__main__':
    from mpi4py import MPI
    import matplotlib.pyplot as plt

    T = 100
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    number = [None, 240, 120, 80, 60][size]
    nx, ny, nz = 200, 200, size*number

    # Split images
    if rank == 0:
        I = default_image(nx, ny, nz)
        for ith, J in enumerate(Worker.split_images(I, size)):
            if ith == 0:
                origin = J
            else:
                comm.Send(J.copy(), dest=ith, tag=10)
    else:
        origin = np.empty((nx, ny, number), dtype='float64')
        comm.Recv(origin, source=0, tag=10)
    plt.figure()
    plt.imshow(origin[:, 100, :], 'gray')
    plt.savefig(f'result/{size}/noised-{rank}.png')

    # Denoising
    J = origin.copy()
    w = Worker(origin)
    *_, channel = J.shape
    for t in range(T):
        if rank == 0 and not t%5:
            print(t, 'out of', T)
        J = w.next(J)

        if rank != size-1:
            sendbuf = J[:, :, channel-1].copy()
            comm.Send(sendbuf, dest=rank+1, tag=20)
        if rank != 0:
            recbuf = np.empty((nx, ny), dtype='float64')
            comm.Recv(recbuf, source=rank-1, tag=20)
            J[:, :, 0] = recbuf

    # Combine images
    if rank == 0:
        result = np.empty((nx, ny, nz), dtype='float64')
        for ith, val in enumerate(Worker.split(range(nz), size)):
            if ith == 0:
                result[:, :, val] = J
            else:
                recbuf = np.empty((nx, ny, number), 'float64')
                comm.Recv(recbuf, source=ith, tag=30)
                result[:, :, val] = recbuf
        plt.figure()
        plt.imshow(result[:, 100, :], 'gray')
        plt.savefig(f'result/{size}/result.png')
    else:
        sendbuf = J.copy()
        comm.Send(sendbuf, dest=0, tag=30)
