#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : model.py
@Time      : 2020/03/11
@Reference : https://lcondat.github.io/software.html
'''
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image



class Denoising:
    def __init__(self, y=None):
        '''Initialize Denoising object.

        Argument:
            - y: numpy.ndarray, default is `self.__default_image()`

        Example:
                >>> from matplotlib.pyplot import cm
                >>> .
                >>> algorithms = 'TV', 'TNV'
                >>> d = Denoising()
                >>> fig = plt.figure()
                >>> length = len(algorithms) + 1
                >>> fig.add_subplot(1, length, 1)
                >>> plt.imshow(d.y, cmap=cm.gray)
                >>> plt.title('Noised Image')
                >>> for ith, algorithm in enumerate(algorithms):
                ...     fig.add_subplot(1, length, ith+2)
                ...     plt.imshow(d.apply(algorithm), cmap=cm.gray)
                ...     plt.title(algorithm)
                >>> plt.show()
        '''
        self.y = self._default_image() if y is None else y
        if isinstance(self.y, np.ndarray):
            self.y = self.y.astype(float) / self.y.max()
        self.shape = self.y.shape
        self.flag = len(self.shape)==2 and self.shape[0]==self.shape[1]


    def __repr__(self):
        '''return `repr(self)`.
        '''
        return f'<Denosing @ {hash(self):#x}>'


    def apply(self, algorithm, **kwargs):
        '''Apply image denoising algorithm.
        '''
        dimension = len(self.shape)
        if dimension == 2:
            api = getattr(self, algorithm, None)
            assert api is not None, f'The algorithm `{algorithm}` does not exist.'
            if self.flag:
                return api(**kwargs)
            else:
                side = max(self.shape)
                I = Image.fromarray(self.y).resize((side, side))
                J = Denoising(np.array(I).T).apply(algorithm, **kwargs)
                K = Image.fromarray(J).resize(self.shape)
                return (np.array(K)).T
        elif dimension == 3:
            x = np.ndarray(self.shape)
            for rgb in range(self.shape[-1]):
                x[:, :, rgb] = Denoising(self.y[:, :, rgb]).apply(algorithm, **kwargs)
            return x
        else:
            raise NotImplementedError


    def TV(self, λ=0.1, τ=0.01, ρ=1.0, epochs=100, y=None):
        r'''Denoising/smoothing a given image y with the isotropic total variation.

        .. math::

            \min ||x-y||_2^2/2 + λ||∇x||_1,2

        Argument:
            - λ: float, lambda
            - τ: float, calculate proximal parameter
            - ρ: float, relaxation parameter in [1,2)
            - epochs: int, number of iterations
            - y: numpy.ndarray, given image, default is `self.y`

        Return:
            - numpy.ndarray, same size as `y`

        Example:
            >>> I = np.zeros((nx, ny))
            >>> J = 0.1*np.random.normal(0, 1, (nx, ny)) + I
            >>> K = TV(y=J)

        Reference:
            The over-relaxed Chambolle-Pock algorithm is described in L. Condat,
            "A primal-dual splitting method for convex optimization involving
            Lipschitzian, proximable and linear composite terms", J. Optimization
            Theory and Applications, vol. 158, no. 2, pp. 460-479, 2013.
        '''
        assert self.flag, 'Maybe you should consider `self.apply`'

        y = self.y if y is None else y
        σ = 1 / (8*τ)

        x2 = y.copy()
        Dh2, Dv2 = self._prox_sigma_g_conj(*self._D(x2), λ) # initialize dual solution

        for ith in range(epochs):
            x = self._prox_tau_f(x2-τ*self._Dadj(Dh2, Dv2), y, τ)
            d = self._D(2*x - x2)
            Dh, Dv = self._prox_sigma_g_conj(Dh2+σ*d[0], Dv2+σ*d[1], λ)
            x2 += ρ * (x-x2)
            Dh2 += ρ * (Dh-Dh2)
            Dv2 += ρ * (Dv-Dv2)

        return x


    def TNV(self, λ=0.1, τ=0.01, ρ=1.0, epochs=100, y=None):
        r'''Denoising/smoothing a given image y with the isotropic total nuclear variation.

        .. math::

            \min ||x-y||_2^2/2 + λ||∇x||_1,* where * is the nuclear norm

        Argument:
            - λ: float, lambda
            - τ: float, calculate proximal parameter
            - ρ: float, relaxation parameter in [1,2)
            - epochs: int, number of iterations
            - y: numpy.ndarray, given image, default is `self.y`

        Return:
            - numpy.ndarray, same size as `y`

        Example:
            >>> I = np.zeros((nx, ny))
            >>> J = 0.1*np.random.normal(0, 1, (nx, ny)) + I
            >>> K = TNV(y=J)

        References:
            This penaly was called the total nuclear variation in * K.M. Holt, Total
            nuclear variation and Jacobian extensions of total variation for vector
            fields, IEEE Trans. Image Proc., vol. 23, pp. 3975–3989, 2014

            It has also been studied with other names in * S. Lefkimmiatis, A. Roussos,
            M. Unser, and P. Maragos, Convex generalizations of total variation based on
            the structure tensor with applications to inverse problems, in Scale Space
            and Variational Methods in Computer Vision, Lecture Notes in Comput. Sci.
            7893, Springer, Berlin, 2013, pp. 48–60. * G Chierchia, N Pustelnik, B
            Pesquet-Popescu, JC Pesquet, "A nonlocal structure tensor-based approach for
            multicomponent image recovery problems", IEEE Trans. Image Proc., 23 (12),
            pp. 5531-5544, 2014. * J. Duran, M. Moeller, C. Sbert, and D. Cremers,
            "Collaborative Total Variation: A General Framework for Vectorial TV Models",
            SIAM J. Imaging Sciences, Vol. 9, No. 1, pp. 116–151, 2016.

            The over-relaxed Chambolle-Pock algorithm used here is described in
            L. Condat, "A primal-dual splitting method for convex optimization involving
            Lipschitzian, proximable and linear composite terms", J. Optimization Theory
            and Applications, vol. 158, no. 2, pp. 460-479, 2013.
        '''
        assert self.flag, 'Maybe you should consider `self.apply`'

        y = self.y if y is None else y
        σ = 1 / (8*τ)

        x2 = y.copy()
        Dh2, Dv2 = np.zeros_like(y), np.zeros_like(y)  # initialize dual solution

        for ith in range(epochs):
            x = self._prox_tau_f(x2-τ*self._Dadj(Dh2, Dv2), y, τ)
            d = self._D(2*x - x2)
            Dh, Dv = self._prox_g(Dh2+σ*d[0], Dv2+σ*d[1], λ)
            x2 += ρ * (x-x2)
            Dh2 += ρ * (Dh-Dh2)
            Dv2 += ρ * (Dv-Dv2)

        return x


    def TGV(self, λ1=0.1, λ2=0.15, τ=0.01, ρ=1.0, epochs=100, y=None):
        r'''Denoising/smoothing a given image y with the second order total generalized
        variation (TGV), defined in K. Bredies, K. Kunisch, and T. Pock, "Total
        generalized variation," SIAM J. Imaging Sci., 3(3), 492-526, 2010.

        .. math::

            \min ||x-y||_2^2/2 + λ1||r||_1,2 + λ2||J(∇x-r)||_1,Frobenius

        Argument:
            - λ1: float, lambda_1
            - λ2: float, lambda_2
            - τ: float, calculate proximal parameter
            - ρ: float, relaxation parameter in [1,2)
            - epochs: int, number of iterations
            - y: numpy.ndarray, given image, default is `self.y`

        Return:
            - numpy.ndarray, same size as `y`

        Example:
            >>> I = np.zeros((nx, ny))
            >>> J = 0.1*np.random.normal(0, 1, (nx, ny)) + I
            >>> K = TGV(y=J)

        References:
            The over-relaxed Chambolle-Pock algorithm is described in L. Condat,
            "A primal-dual splitting method for convex optimization involving
            Lipschitzian, proximable and linear composite terms", J. Optimization Theory
            and Applications, vol. 158, no. 2, pp. 460-479, 2013.
        '''
        raise NotImplementedError

        assert self.flag, 'Maybe you should consider `self.apply`'

        y = self.y if y is None else y
        σ = 1 / (72*τ)

        x2 = y.copy()
        Dh2, Dv2 = self._prox_sigma_g_conj(*self._D(x2), λ) # initialize dual solution

        for ith in range(epochs):
            x = self._prox_tau_f(x2-τ*self._Dadj(Dh2, Dv2), y, τ)
            d = self._D(2*x - x2)
            Dh, Dv = self._prox_sigma_g_conj(Dh2+σ*d[0], Dv2+σ*d[1], λ)
            x2 += ρ * (x-x2)
            Dh2 += ρ * (Dh-Dh2)
            Dv2 += ρ * (Dv-Dv2)

        return x


    def add_noise(self, μ=0.5, σ=0.1):
        '''Add normal noise with `μ` and `σ`.

        Example:
            >>> d = Denoising().add_noise(0, 0.1)
        '''
        self.y += self._noise(self.y, μ, σ)
        return self


    def _default_image(self, nx=200, ny=200, μ=0.5, σ=0.1):
        index = lambda n, l, r: slice(int(n*l), int(n*r))
        x = np.zeros((nx, ny))
        x[index(nx, 0.375, 0.75), index(ny, 0.375, 0.75)] = 1
        y = self._noise(x, μ, σ) + x
        return y


    def _noise(self, y, μ=0.5, σ=0.1):
        return np.random.normal(μ, σ, y.shape)


    def _debug(self, **kwargs):
        import IPython
        import sys

        IPython.embed(user_ns=sys._getframe(1).f_locals, colors='Linux', **kwargs)


    def _D(self, x):
        # ∇
        width, height, *_ = self.shape  # 2-dimension
        Dh = np.concatenate((np.diff(x, 1, 0), np.zeros((1, width))), axis=0)
        Dv = np.concatenate((np.diff(x, 1, 1), np.zeros((height, 1))), axis=1)
        return Dh, Dv


    def _Dadj(self, Dh, Dv, index=slice(0, 1)):
        D2h = np.concatenate((Dh[index, :], np.diff(Dh, 1, 0)), axis=0)
        D2v = np.concatenate((Dv[:, index], np.diff(Dv, 1, 1)), axis=1)
        return -(D2h + D2v)


    def _prox_tau_f(self, x, y, τ):
        return (x + τ*y) / (1 + τ)


    def _prox_sigma_g_conj(self, Dh, Dv, λ):
        TV = np.sqrt(Dh**2 + Dv**2) / λ
        TV = TV.clip(1, None)  # limit the values to [1, inf]
        return Dh/TV, Dv/TV


    def _prox_g(self, Dh, Dv, λ):
        s = (Dh**2).sum(axis=1) - (Dv**2).sum(axis=1)
        theta = np.arctan2(2*(Dh*Dv).sum(axis=1), s)/2
        c, s = np.cos(theta), np.sin(theta)
        Dh2, Dv2 = Dh*c+Dv*s, Dv*c-Dh*s
        scale = 1 - λ / np.sqrt(Dh**2+Dv**2).clip(λ)
        Dh2 *= scale
        Dv2 *= scale
        return Dh-Dh2*c+Dv2*s, Dv-Dv2*c-Dh2*s



if __name__ == '__main__':
    from matplotlib.pyplot import cm

    algorithms = 'TV', 'TNV', 'TGV'

    d = Denoising()
    fig = plt.figure()
    length = len(algorithms) + 1
    fig.add_subplot(1, length, 1)
    plt.imshow(d.y, cmap=cm.gray)
    plt.title('Noised Image')
    for ith, algorithm in enumerate(algorithms):
        fig.add_subplot(1, length, ith+2)
        plt.imshow(d.apply(algorithm), cmap=cm.gray)
        plt.title(algorithm)
    plt.show()
