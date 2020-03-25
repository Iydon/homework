import numpy as np

from numpy import array, diag, divide, exp, matrix, power, zeros
from numpy.linalg import inv, norm


class logistic_regression_IRLS(object):
    """
    Maximum likelihood approach for logistic regression.
    """
    def __init__(self):
        self.w = None

    def fit(self, X, y, w0=None, erf=None, maxit=None, display=None):
        self.__newton_raphson(X, y, w0, erf, maxit, display)

    def predict(self, X):
        y = X * self.w
        return array((y>0).astype(int).T)[0]
        
    def __newton_raphson(self, X, y, w0, erf, maxit, display):
        """
        Args:
            X:   nxd matrix.
            y:   nx1 column vector.
            w0:  dx1 column vector.
            erf: error function with two parameters.
                 erf = lambda old,new: ...
        """
        # Pre-process
        X   = matrix(X)
        n,d = X.shape
        y   = matrix(y).reshape(n, 1)
        if w0==None:
            w0 = zeros((d, 1))
        if erf==None:
            erf = lambda old,new: norm(old-new,2)<1e-6
        if maxit==None:
            maxit = 64
        if display==None:
            display = False
        w1 = zeros((d, 1))
        ex = zeros((n, 1))
        # Iterations
        for i in range(maxit):
            ex = exp(X*w0).T
            D  = diag(array(ex/power(1+ex,2))[0])
            w1 = w0 + inv(X.T*D*X)*X.T*(y-(ex/(1+ex)).T)
            if erf(w0, w1):
                if display:
                    print("Convergence @ the %d iteration(s)."%i)
                break
            w0 = w1
        self.w = w1


"""
from sklearn.linear_model import LogisticRegression as Regression


X = np.random.rand(20, 2)-0.5
y = (np.sum(X,1)>0).astype(int)

model_1 = logistic_regression_IRLS()
model_1.fit(X, y)
y_1 = model_1.predict(X)

model_2 = Regression(solver="lbfgs")
model_2.fit(X, y)
y_2 = model_2.predict(X)

dy_1 = norm(y_1-y, 2)
dy_2 = norm(y_2-y, 2)

print(dy_1, dy_2)
"""
