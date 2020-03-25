# -*- encode: utf-8 -*-
from sklearn.ensemble import AdaBoostRegressor, BaggingRegressor, \
    ExtraTreesRegressor, GradientBoostingRegressor, IsolationForest

from sklearn.gaussian_process import GaussianProcessRegressor

from sklearn.linear_model import ElasticNetCV, HuberRegressor, \
    LassoLarsCV, LogisticRegression, PassiveAggressiveRegressor, \
    RANSACRegressor, RidgeCV, SGDRegressor, TheilSenRegressor

from sklearn.neighbors import KNeighborsRegressor, RadiusNeighborsRegressor

from sklearn.neural_network import MLPRegressor


regressors = [AdaBoostRegressor, BaggingRegressor, ExtraTreesRegressor,
    GradientBoostingRegressor, IsolationForest, GaussianProcessRegressor,
    ElasticNetCV, HuberRegressor, LassoLarsCV, LogisticRegression,
    PassiveAggressiveRegressor, RANSACRegressor, RidgeCV, SGDRegressor,
    TheilSenRegressor, KNeighborsRegressor, RadiusNeighborsRegressor,
    MLPRegressor]
