# -*- encode: utf-8 -*-
from decimal import Decimal
from typing import Callable
from random import random, randint, choice, choices, gauss


def minmax(min_:[int, float], value:[int, float], max_:[int, float]) -> [int, float]:
    '''Specify the range.'''
    if min_ > value:
        return min_
    elif value > max_:
        return max_
    else:
        return value

# ======================= models.py =======================
def longitude() -> Decimal:
    '''纬度'''
    a = 3. + 51/60
    b = 53. + 33/60
    return Decimal(random_(a, b))

def latitude() -> Decimal:
    '''经度'''
    a = 73. + 33/60
    b = 135. + 5/60
    return Decimal(random_(a, b))

def random_(a:float, b:float) -> float:
    '''Random from `a` to `b`.
    '''
    return (b-a)*random() + a

with open('region.tsv', 'r') as f:
    regions = [line.split('\t') for line in f.readlines()]
def latlng() -> Decimal:
    '''经度, 纬度'''
    while True:
        city, lat, lng = choice(regions)
        if city.endswith('市') or '香港' in city or '澳门' in city or '台湾' in city:
            break
    return Decimal(lat), Decimal(lng)


language = 'zh'

translation = {
    'airport': {
        'zh': '机场',
        'en': ' airport '
    },
    'longitude': {
        'zh': longitude,
    },
    'latitude': {
        'zh': latitude,
    },
    'latlng':{
        'zh': latlng,
    },
    'location': {
        'zh': (35.7, 104.3),
    }
}


# ======================= map.py =======================
time_limit = 30 * 60
distance_to_weights = lambda x: x ** .5


# ======================= data.py =======================
def airport_capacity() -> Callable:
    weight = (10, 27, 29)
    capacity = (gauss(178, 21), gauss(55, 6), gauss(30, 2))

    func, = choices(capacity, weights=weight)
    return max(0, round(func))


data_file = 'data.pickle'

city_number = 45

city_capacity = lambda: max(1, round(gauss(5, 1)))
aircraft_capacity = lambda: max(1, round(gauss(150, 30)))
aircraft_speed = lambda: max(1, gauss(500, 50))
aircraft_capacity_ratio = lambda: minmax(0, gauss(0.5, 0.1), 1)
people_number_ratio = lambda: minmax(0, gauss(0.7, 0.1), 1)


# ======================= map.py =======================
html_file = 'world_map_airports.html'


# ======================= main.py =======================
def randbool() -> bool:
    '''Random boolean.
    '''
    return bool(randint(0, 1))

def randgauss(mu:float, sigma:float) -> float:
    '''Random gauss distribution.
    '''
    return minmax(0.0, gauss(mu, sigma), 1.0)

def path_number(is_day:bool=True) -> int:
    '''Return path number with different `is_day`.
    '''
    mu, sigma = (2, 1) if is_day else (1, 1)
    return max(0, round(gauss(mu, sigma)))

def aircraft_number(is_day:bool=True) -> int:
    '''Return aircraft number with different `is_day`.
    '''
    mu, sigma = (2, 1) if is_day else (1, 1)
    return max(0, round(gauss(mu, sigma)))
