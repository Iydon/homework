#!/usr/bin/python3
__all__ = ('debug', )


import IPython
import sys


def debug(**kwargs):
    local = sys._getframe(1).f_locals
    IPython.embed(user_ns=local, colors='Linux', **kwargs)
