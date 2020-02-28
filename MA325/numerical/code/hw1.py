def question_1():
    # packages
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import axes3d
    from matplotlib import cm
    import numpy as np

    # parameters
    t = np.linspace(-1.2, 1.2, 512)
    X, Y = np.meshgrid(t, t)
    norms = {
        '$\infty$-norm': lambda x, y: max(abs(x), abs(y)),
        '1-norm': lambda x, y: abs(x)+abs(y),
        '2-norm': lambda x, y: np.sqrt(x**2+y**2),
    }
    zlim = 0, 1.2
    figsize = 9, 3

    # body
    length = len(norms)
    Z = np.zeros_like(X)
    fig = plt.figure(figsize=figsize)
    for ith, (name, func) in enumerate(norms.items()):
        for jth in range(Z.size):
            value = func(X.flat[jth], Y.flat[jth])
            Z.flat[jth] = value if value<=1 else np.nan
        ax = fig.add_subplot(1, length, ith+1, projection='3d')
        ax.plot_surface(X, Y, Z, alpha=0.3)
        ax.contour(X, Y, Z, zdir='z', offset=zlim[0], cmap=cm.coolwarm)
        ax.set_zlim(*zlim)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(name)
    plt.show()


if __name__ == '__main__':
    question_1()
