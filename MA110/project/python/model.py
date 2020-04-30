# built-in
from itertools import repeat
from os import listdir
from os.path import exists, join
from time import time
# multi-processing and optimize
import multiprocessing as mp
# matlab interface and numerical
from array import array
import numpy as np
try:
    from scipy.io import loadmat
except:
    pass


def load_row_col_paint(convert=False):
    '''Load data from `mat` and convert to `npz`.
    '''
    def f(x):  # squeeze
        y = x.tolist()
        return tuple(y[0])if y else tuple()
    dir_name = join('..', 'data')
    flag_name = '.flag'
    flag = exists(join(dir_name, flag_name))
    for file_name in listdir(dir_name):
        path = join(dir_name, file_name)
        if flag:
            if path.endswith('.npz'):
                data = np.load(path, allow_pickle=True)
            else:
                continue
        else:
            data = loadmat(path)
            if convert:
                np.savez(path.replace('.mat', '.npz'), **data)
        row = tuple(map(f, data['rKey'][0]))
        col = tuple(map(f, data['cKey'][0]))
        yield row, col, data['Paint']
    if convert and not flag:
        with open(join(dir_name, flag_name), 'a+') as f:
            f.write(f'{time()}\n')


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
    kwargs = dict(threshold=64, scale=2, n_steps=-1, n_processes=0)
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

    API:
        - property
            - paint
            - is_finished
            - is_initial
        - function
            - doit()
            - equal_to(numpy.ndarray)
        - classmethod
            - _inverse(numpy.ndarray)
    '''
    def __init__(self, row, col, threshold=64, scale=2, n_steps=-1, n_processes=0):
        '''
        Argument:
            - row: tuple[tuple]
            - col: tuple[tuple]
            - threshold: int, see `self._intersection`
            - scale: int, multiply `self._threshold` when algorithm fails
            - n_steps: int, max steps
            - n_processes: int, whether to use `multiprocessing`
        '''
        self._row = row
        self._col = col
        self._iths = set(range(len(row)))
        self._jths = set(range(len(col)))
        self._threshold = threshold
        self._scale = scale
        self._steps = n_steps
        self._processes = n_processes
        self._paint = -np.ones((len(row), len(col)), dtype=int)

    def __repr__(self):
        return f'<PaintItBack @ {hash(self):#x}>'

    @property
    def paint(self):
        return self._paint

    @property
    def is_finished(self):
        return not (self._paint==-1).any()

    @property
    def is_initial(self):
        return (pib.paint==-1).all()

    def equal_to(self, paint):
        try:
            return (self._paint==paint).all()
        except:
            return False

    def doit(self):
        if self._processes:
            self._doit_parallel()
        else:
            self._doit_serial()
        assert self.is_finished, 'Algorithm fails.'

    def _doit_serial(self):
        previous_hash = current_hash = 0
        while self._steps != 0:
            self._steps -= 1
            current_hash = self._paint.sum()
            for ith in self._iths.copy():
                row = self._row[ith]
                self._intersection(self._paint[ith, :], row, ith=ith)
            for jth in self._jths.copy():
                col = self._col[jth]
                self._intersection(self._paint[:, jth], col, jth=jth)
            if self.is_finished:
                break
            if (current_hash==previous_hash).all():
                self._threshold *= self._scale
            previous_hash = current_hash

    def _doit_parallel(self):
        previous_hash = current_hash = 0
        f = self._intersection
        with Pool(self._processes) as p:
            while self._steps != 0:
                self._steps -= 1
                current_hash = self._paint.sum()
                for ith in self._iths.copy():
                    self._paint[ith, :] = p.apply_async(f,
                        args=(self._paint[ith, :], self._row[ith]),
                        kwds=dict(ith=ith)
                    ).get()
                for jth in self._jths.copy():
                    self._paint[:, jth] = p.apply_async(f,
                        args=(self._paint[:, jth], self._col[jth]),
                        kwds=dict(jth=jth)
                    ).get()
                if self.is_finished:
                    break
                if (current_hash==previous_hash).all():
                    self._threshold *= self._scale
                previous_hash = current_hash

    def _intersection(self, origin, choices, ith=None, jth=None):
        '''Intersection of all possibilities.

        Argument:
            - origin: numpy.ndarray
            - choices: tuple

        Return:
            - numpy.ndarray
        '''
        # check wheather `ith` and `jth` is valid
        # if (isinstance(ith, int) and ith not in self._iths) \
        #         or (isinstance(jth, int) and jth not in self._jths) \
        #         or (not choices):
        if not choices:
            return origin
        m = len(choices) + 1
        n = len(origin) - sum(choices) - m + 2
        count = [0] * len(origin)
        total = 0
        f = lambda ns: self._expand(self._convert_choices(choices, ns))
        for numbers in self._n_balls_m_boxes(n, m):
            for o, value in zip(origin, f(numbers)):
                if 0 <= o != value:
                    break
            else:
                if total > self._threshold:
                    return origin
                total += 1
                for kth, value in enumerate(f(numbers)):
                    count[kth] += value
        for kth, value in enumerate(count):
            if value == 0:
                origin[kth] = 0
            elif value == total:
                origin[kth] = 1
        if (origin!=-1).all():
            isinstance(ith, int) and self._iths.remove(ith)
            isinstance(jth, int) and self._jths.remove(jth)
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
            - numbers: iterable
        '''
        numbers = iter(numbers)
        yield -next(numbers)
        for chioce in choices[:-1]:
            yield chioce
            yield -1 - next(numbers)
        yield choices[-1]
        yield -next(numbers)

    def _convert_choices_and_expand(self, chioces, numbers):
        '''Combine and optimize two functions.

        Note:
            - cannot improve efficiency
        '''
        ith = -1
        for kth in range(len(chioces)):
            ith += numbers[kth] + 1
            yield from range(ith, ith+chioces[kth])
            ith += chioces[kth]

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
    try:
        from model import PaintItBack
    except:
        pass

    for row, col, paint in load_row_col_paint():
        pib = PaintItBack(row, col, threshold=64, scale=2, n_steps=-1, n_processes=0)
        with Timer() as t:
            pib.doit()
        shape = '{}x{}'.format(*paint.shape)
        flag = '√' if pib.equal_to(paint) else '×'
        elapse = f'{t.elapse:>4.2f}s = {1000*t.elapse:>8.2f}ms'
        print(f'{shape}\t{flag}\t{elapse}')
