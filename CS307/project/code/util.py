#!/usr/bin/python3
__all__ = ('debug', )


import IPython
import itertools
import sys


def debug(**kwargs):
    local = sys._getframe(1).f_locals
    IPython.embed(user_ns=local, colors='Linux', **kwargs)


def sizeof(obj, handlers=dict(), verbose=False):
    '''Returns the approximate memory footprint an object and all of its contents.

    :Description:
    Automatically finds the contents of the following builtin containers and
    their subclasses: tuple, list, dict, set and frozenset. To search other
    containers, add handlers to iterate over their contents.

    :Example:
    >>> d = dict(a=1, b=2, c=3, d=[4,5,6,7], e='a string of chars')
    >>> print(sizeof(d, verbose=True))
    '''
    def _sizeof(obj, handlers=dict(), seen=set()):
        if id(obj) in seen:
            return 0
        seen.add(id(obj))
        s = sys.getsizeof(obj)
        if verbose:
            print(s, type(obj), repr(obj))
        for T, handler in handlers.items():
            if isinstance(obj, T):
                f = lambda o: _sizeof(o, handlers, seen)
                s += sum(map(f, handler(obj)))
                break
        return s

    default_handlers = {
        dict: lambda d: itertools.chain.from_iterable(d.items()),
        frozenset: iter, list: iter, set: iter, tuple: iter,
    }
    default_handlers.update(handlers)
    return _sizeof(obj, default_handlers)
