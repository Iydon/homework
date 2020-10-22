from timeit import timeit

statement = '''
from math import sqrt, sin, cos, log, pi, e

xx = (1+2) * (-3.14e-2+sqrt(pi)) / (sin(cos(1+pi))+e)
_ = log(pi)
yy = (xx+_) ; yy *= (e+1)
print(yy)
'''

second = timeit(statement, number=1)
print(f'Time has elapsed {1e6*second:.2f}µs ≈ {1e3*second:.2f}ms ≈ {second:.2f}s.')
