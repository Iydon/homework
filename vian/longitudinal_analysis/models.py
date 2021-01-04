import json
import hashlib
import pathlib

import numpy as np
import pandas as pd

from scipy import stats

from sklearn.base import BaseEstimator
from sklearn.linear_model import LinearRegression


class Dataset:
    '''纵向数据分析的数据集
    '''
    def __init__(self, dirname='data', metaname='meta.json', encoding='utf-8'):
        self._dir = pathlib.Path(dirname)
        self._meta = tuple(filter(
            lambda item: item['filename'],  # determine whether it is a sample item
            json.loads((self._dir/metaname).read_text(encoding=encoding)))
        )

    def at(self, ith, xy=False):
        '''
        Return:
            {group: (x, y)} if xy else (meta, data)
        '''
        meta = self._meta[ith]
        content = (self._dir/meta['filename']).read_bytes()
        if hashlib.md5(content).hexdigest() != meta['filename']:
            raise Exception('MD5CheckFailed')
        data = getattr(pd, 'read_'+meta['format'])(content, **meta['kwargs'])
        if xy:
            if not meta['xyz']:
                raise NotImplementedError
            data = {
                id: (
                    group[meta['xyz']['x']],
                    group[meta['xyz']['y']]
                )
                for id, group in data.groupby(meta['xyz']['z'])
            }
        return {key: meta[key] for key in ('title', 'description', 'header', 'xyz', 'attribute')}, data

    def filter(self, xy=False, **kwargs):
        for ith, meta in enumerate(self._meta):
            if len(kwargs) == sum(
                key in meta['attribute'] and meta['attribute'][key]==val
                for key, val in kwargs.items()
            ):
                yield self.at(ith, xy)

    def __getitem__(self, ith):
        return self.at(ith)

    def __iter__(self):
        for ith in range(len(self)):
            yield self.at(ith)

    def __len__(self):
        return len(self._meta)

    def __repr__(self):
        return f'<Dataset({len(self)}) @ {hash(self):#x}>'


class Symbol:
    '''广义线性模型的符号表示：Y~X
    '''
    def __init__(self, meta=None, data=None):
        self._meta = meta
        self._data = None if data is None else pd.DataFrame(data)
        self._hash = self._md5(meta) if meta else None
        self._names = [list(), list()]  # [Y, X]
        self._model = None

    def __getitem__(self, key):
        result = Symbol(self._meta, self._data[key])
        result._names[0].append(key)
        return result

    def __add__(self, value):
        assert self._hash == value._hash
        result = Symbol(self._meta, None)
        result._data = pd.concat((self._data, value._data), axis=1)
        result._names[0] = self._names[0] + value._names[0]
        return result

    def __eq__(self, value):
        assert self._hash == value._hash
        result = Symbol(self._meta, None)
        result._data = pd.concat((self._data, value._data), axis=1)
        result._names = [self._names[0], value._names[0]]
        return result

    def __repr__(self):
        statement = ', '.join(self._names[0])
        if self._names[1]:
            statement += ' ~ ' + ' + '.join(self._names[1])
        return statement

    @property
    def data(self):
        '''多元统计数据
        '''
        return self._data

    @property
    def columns(self):
        '''按 X，Y 返回数据表头
        '''
        return dict(x=self._names[1], y=self._names[0])

    @property
    def model(self):
        '''sklearn 线性模型
        '''
        if self._model is None:
            self._model = self.fit()
        return self._model
    @model.setter
    def model(self, value):
        assert isinstance(value, BaseEstimator)
        self._model = value
    @model.deleter
    def model(self):
        self._model = None

    @property
    def xy(self):
        '''按 X，Y 返回数据
        '''
        return self._data[self._names[1]], self._data[self._names[0]]

    def apply(self, function, name=None, **kwargs):
        '''单元数据变换
        '''
        mapper = {
            column: f'{name or function.__name__}({column})'
            for column in self._names[0]
        }
        result = Symbol(self._meta, None)
        result._data = self._data.apply(function, **kwargs).rename(columns=mapper)
        result._names[0] += mapper.values()
        return result

    def interact(self, function, name, **kwargs):
        '''多元数据交互
        '''
        result = Symbol(self._meta, None)
        result._data = pd.DataFrame(self._data.apply(function, axis=1, **kwargs))
        result._data.columns = [name]
        result._names[0] += result._data.columns.to_list()
        return result

    def ones(self):
        '''A new DataFrame, filled with ones
        '''
        result = Symbol(self._meta, pd.DataFrame(1, index=self._data.index, columns=list('1')))
        result._names[0].append('1')
        return result

    def fit(self, model=LinearRegression, **kwargs):
        '''Fit linear model
        '''
        result = model(**kwargs)
        result.fit(*self.xy)
        return result

    def describe(self):
        '''Generate descriptive statistics

        Reference:
            - https://stats.stackexchange.com/questions/262834/why-does-scipy-use-wald-statistic-t-test-as-opposed-to-wald-statistic-wald-t
        '''
        expression = repr(self)
        formula = '[{0}] = {2} + {1}'.format(
            ', '.join(self._names[0]), self.model.intercept_,
            ' + '.join(map(lambda x: f'{x[0]}*{x[1]}', zip(self.model.coef_.T, self._names[1])))
        )
        coefficients = dict()
        for ith, name in enumerate(self._names[0]):
            coefficients[name] = pd.DataFrame(index=self._names[1])
            coefficients[name]['estimate'] = self.model.coef_[ith]
            coefficients[name]['wald'] = tuple(
                self._wald(
                    self._data[n].to_numpy(), self._data[self._names[0][ith]].to_numpy()
                ) for jth, n in enumerate(self._names[1])
            )
            coefficients[name]['p'] = tuple(
                stats.ttest_ind(
                    self._data[self._names[0][ith]], self._data[n]
                ).pvalue for n in self._names[1]
            )
        _locals = locals()
        return {key: _locals[key] for key in ('expression', 'formula', 'coefficients')}

    def _md5(self, obj):
        return hashlib.md5(repr(obj).encode()).hexdigest()

    def _wald(self, x, y):
        length = len(x)
        x_mean, y_mean = np.mean(x), np.mean(y)
        x_diff, y_diff = x-x_mean, y-np.mean(y)
        slope = np.sum(x_diff*y_diff) / np.sum(x_diff**2)
        intercept = y_mean - slope*x_mean
        error_std = np.sqrt(np.sum((y-(slope*x+intercept))**2)/(length-2))
        x_std = np.sqrt(np.sum(x_diff**2)/length)
        return slope*x_std*np.sqrt(length)/error_std
