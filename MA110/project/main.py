# built-in
from itertools import repeat
from os import listdir
from os.path import join
from time import time
# multi-processing
import multiprocessing as mp
# matlab interface and numerical
from array import array
import numpy as np
from scipy.io import loadmat


def load_row_col_paint():
    def f(x):  # squeeze
        y = x.tolist()
        return tuple(y[0])if y else tuple()
    dir_name = 'data'
    for file_name in listdir(dir_name):
        path = join(dir_name, file_name)
        data = loadmat(path)
        # __import__('IPython').embed(colors='Linux')
        row = tuple(map(f, data['rKey'][0]))
        col = tuple(map(f, data['cKey'][0]))
        yield row, col, data['Paint']


def api(row, col, **kwargs):
    pib = PaintItBack(row, col, **kwargs)
    pib.doit()
    return pib.paint


def matlab_api(row, col):
    '''MATLAB API
    '''
    def f(x):
        if isinstance(x, float):
            return (int(x), )
        else:
            return tuple(map(int, x))
    g = lambda x: array('d', x)
    # default kwargs
    kwargs = dict(threshold=64, n_processes=0)
    result = api(tuple(map(f, row)), tuple(map(f, col)), **kwargs)
    return tuple(map(g, result.tolist()))


class Timer:
    '''Timer

    Example:
        >>> with Timer() as t:
        ...     <statement>
        ... print(t.elapse)
    '''
    def __enter__(self):
        self._tic_toc = time()
        return self

    def __exit__(self, type, value, traceback):
        self._tic_toc = time() - self._tic_toc

    @property
    def elapse(self):
        return self._tic_toc


class Pool:
    '''Pool
    '''
    def __init__(self, processes=None):
        self._processes = mp.cpu_count() \
            if processes is None else processes

    def __enter__(self):
        if self._processes:
            self._pool = mp.Pool(processes=self._processes)
            return self._pool

    def __exit__(self, type, value, traceback):
        if self._processes:
            self._pool.close()
            self._pool.join()


class PaintItBack:
    '''Paint it back game.
    '''
    def __init__(self, row, col, threshold=64, n_processes=0):
        '''
        Argument:
            - row: tuple[tuple]
            - col: tuple[tuple]
            - threshold: int, see `self._intersection`
            - n_processes: int, whether to use `multiprocessing`
        '''
        self._row = row
        self._col = col
        self._threshold = threshold
        self._paint = - np.ones((len(row), len(col)), dtype=int)
        self._processes = n_processes

    def __repr__(self):
        return f'<PaintItBack @ {hash(self):#x}>'

    @property
    def paint(self):
        return self._paint

    @property
    def is_finished(self):
        return not (self._paint==-1).any()

    @property
    def is_initialized(self):
        return (pib.paint==-1).all()

    def doit(self):
        # simple fill algorithm
        if self._processes:
            self.doit_parallel()
        else:
            self.doit_serial()
        if self.is_finished:
            return None
        # todo
        raise NotImplementedError

    def doit_serial(self):
        while True:
            comparison = self._paint.copy()
            for ith, row in enumerate(self._row):
                self._intersection(self._paint[ith, :], row)
            for jth, col in enumerate(self._col):
                self._intersection(self._paint[:, jth], col)
            if (comparison==self._paint).all():
                break

    def doit_parallel(self):
        f = self._intersection
        with Pool(self._processes) as p:
            while True:
                comparison = self._paint.copy()
                for ith, row in enumerate(self._row):
                    args = self._paint[ith, :], row
                    self._paint[ith, :] = p.apply_async(f, args=args).get()
                for jth, col in enumerate(self._col):
                    args = self._paint[:, jth], col
                    self._paint[:, jth] = p.apply_async(f, args=args).get()
                if (comparison==self._paint).all():
                    break

    def _intersection(self, origin, choices):
        '''Intersection of all possibilities.

        Argument:
            - origin: numpy.ndarray
            - choices: tuple

        Return:
            - numpy.ndarray
        '''
        if not choices:
            return origin
        m = len(choices) + 1
        n = len(origin) - sum(choices) - m + 2
        count = [0] * len(origin)
        total = 0
        f = lambda ns: self._expand(self._convert_choices(choices, ns))
        for numbers in self._n_balls_m_boxes(n, m):
            for ith, value in enumerate(f(numbers)):
                if 0 <= origin[ith] != value:
                    break
            else:
                total += 1
                if total > self._threshold:
                    return origin
                for ith, value in enumerate(f(numbers)):
                    count[ith] += value
        for ith, value in enumerate(count):
            if value == 0:
                origin[ith] = 0
            elif value == total:
                origin[ith] = 1
        return origin

    def _expand(self, marks):
        '''Expand marks.

        Argument:
            marks: iterable
        '''
        for mark in marks:
            if mark > 0:
                yield from repeat(1, mark)
            elif mark < 0:
                yield from repeat(0, -mark)

    def _convert_choices(self, choices, numbers=repeat(0)):
        '''Convert chioces to marks.

        Argument:
            - chioces: tuple
            - number: iterable
        '''
        numbers = iter(numbers)
        yield -next(numbers)
        for chioce in choices[:-1]:
            yield chioce
            yield -1 - next(numbers)
        yield choices[-1]
        yield -next(numbers)

    def _n_balls_m_boxes(self, n, m):
        '''All possibilities of n balls and m boxes.

        Reference:
            - https://www.cnblogs.com/zwfymqz/p/9724918.html#_label2_1
        '''
        def nested(n, m, r):  # nested function
            if m == 1:
                r[-1] = n
                yield r
            else:
                for i in range(n+1):
                    r[-m] = i
                    yield from nested(n-i, m-1, r)
        # possibilities
        yield from nested(n, m, [0]*m)

    def _nchoosek(self, n, k):
        '''n choose k.
        '''
        f = np.math.factorial
        return f(n) // f(k) // f(n-k)

    @classmethod
    def _inverse(self, paint):
        '''
        Argument:
            - paint: numpy.ndarray

        Return:
            - row: tuple
            - col: tuple
        '''
        def cn(line, count=0):  # count nonzero
            for value in line:
                if value:
                    count += 1
                elif count != 0:
                    yield count
                    count = 0
            if count != 0:
                yield count
        # inverse paint it back algorithm
        width, height = paint.shape
        row = tuple(tuple(cn(paint[ith, :])) for ith in range(width))
        col = tuple(tuple(cn(paint[:, jth])) for jth in range(height))
        return row, col


if __name__ == '__main__':
    for row, col, paint in load_row_col_paint():
        pib = PaintItBack(row, col, threshold=64, n_processes=0)
        with Timer() as t:
            pib.doit()
        shape = '{}x{}'.format(*paint.shape)
        flag = '√' if (pib.paint==paint).all() else '×'
        elapse = f'{t.elapse:>4.2f}s = {1000*t.elapse:>8.2f}ms'
        print(shape, flag, elapse, sep='\t')
