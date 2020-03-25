# -*- encode: utf-8 -*-
from prettytable import PrettyTable

import numpy as np
from sklearn import metrics
from sklearn import preprocessing
from sklearn import decomposition

from color import color


def calc_accuracy(y_true, y_predict, display=True):
    """Analysis the score with sklearn.metrics.
    This module includes score functions, performance metrics
    and pairwise metrics and distance computations.

    Parameters
    ==========
    y_true:    numpy.array
    y_predict: numpy.array
    display:   Boolean

    Return
    ======
    result: Dict{name:value}

    Examples
    ========
    >>> result = analysis(y_true, y_predict, display=True)
    """
    score  = ["explained_variance_score", "r2_score"]
    error  = ["max_error", "mean_absolute_error", "mean_squared_error",
              "mean_squared_log_error", "median_absolute_error"]
    result = dict()
    names  = ["score", "error"]
    ignore = []
    for name in names:
        result[name] = dict()
        for item in locals()[name]:
            try:
                result[name][item] = getattr(metrics, item)(y_true, y_predict)
            except Exception as e:
                print(color(("↓ %s has been removed since `%s`." % \
                    (item.capitalize(), e))))
                ignore.append(item)
    if display:
        tabu,numerical = None, None
        for name in names:
            tabu = PrettyTable(["Name of %s"%color(name), "Value"])
            for item in locals()[name]:
                if item in ignore:
                    continue
                numerical = "%.3e" % result[name][item]
                tabu.add_row([color(item,"青"), numerical])
            print(tabu)
    return result


def dimensionality_reduction(data, n_dim=None, thold=0.9, method="PCA", help_me=False, **arg_d):
    """Dimensionality reduction

    Parameters
    ==========
    data:    n_samples x n_features
    n_dim:   n-dimension
    thold:   Float, threshold
    method:  String, decomposition method
             {"主成分分析":   ["PCA", "IncrementalPCA", "KernelPCA",
                               "MiniBatchSparsePCA", "SparsePCA",
                               "TruncatedSVD"],
              "因子分析":     ["FactorAnalysis"],
              "独立成分分析": ["FastICA"],
              "字典学习":     ["DictionaryLearning",
                               "MiniBatchDictionaryLearning"],
              "高级矩阵分解": ["LatentDirichletAllocation", "NMF"],
              "其他矩阵分解": ["SparseCoder"]}
    help_me: Boolean
    arg_d:   Dict[args of sklearn.decomposition.?]
             Dict{name:value}

    Return
    ======
    decomodel: decomposition model
    data_:     data after transform

    Examples
    ========
    >>> dec,data_ = dimensionality_reduction(data, thold=0.9, method="PCA"):

    Reference
    =========
    - [Zhihu](https://zhuanlan.zhihu.com/p/59591749)
    - [Oreilly](https://www.oreilly.com/learning/an-illustrated-introduction-to-the-t-sne-algorithm)
    - [Scikit](http://lijiancheng0614.github.io/scikit-learn/modules/generated/sklearn.decomposition.PCA.html)
    """
    methods = ["DictionaryLearning", "FactorAnalysis", "FastICA",
               "IncrementalPCA", "KernelPCA", "LatentDirichletAllocation",
               "MiniBatchDictionaryLearning", "MiniBatchSparsePCA", "NMF",
               "PCA", "SparseCoder", "SparsePCA", "TruncatedSVD"]
    if method not in methods:
        raise NameError("Method %s not in sklearn.decomposition"%color(method))
    alias = getattr(decomposition, method)
    if n_dim is not None:
        decomodel = alias(n_components=n_dim, **arg_d)
        decomodel.fit(data)
        return decomodel, decomodel.transform(data)
    elif thold is not None:
        decomodel = alias(**arg_d)
        decomodel.fit(data)
        if "explained_variance_ratio_" in dir(decomodel):
            ratio = decomodel.explained_variance_ratio_
            index = np.sum(np.cumsum(ratio) < thold)
            decomodel.components_ = decomodel.components_[:index]
        else:
            raise NotImplementedError("TODO")
        return decomodel, decomodel.transform(data)
    else:
        raise ValueError("There must be at most two None in n_dim and thold.")


def data_preprocess(*argl, **argd):
    """TODO
    """
    raise NotImplementedError("TODO")
