# -*- encode: utf-8 -*-
from typing import List, Tuple, Callable
import numpy as np

from models import Aircraft, Airport, City, Time
from settings import time_limit, time_limit, distance_to_weights


# Phantom class
class Airline: pass
class Symmetric: pass


class Airline:
    def __init__(self, cities:List[City], time_limit:int, distance_to_weights:Callable):
        '''Initialize Airline.

        Arguments:
        ==========
            cities: List[City, ...]
            time_limit: Integer (second)
            distance_to_weights: Callable

        Returns:
        ========
            None
        '''
        self.cities = cities
        self.city_number = len(cities)
        self.time_limit = time_limit
        self.distance_to_weights = distance_to_weights
        self.distances = Symmetric(self.city_number)

        for ith in range(self.city_number):
            self.distances[ith, ith] = None
            for jth in range(ith+1, self.city_number):
                self.distances[ith, jth] = self.distance_from_ith_jth(ith, jth)

    def __repr__(self) -> str:
        '''Return repr(self).
        '''
        return '<Airline with {} path(s)>'.format(len(self))

    def __len__(self) -> int:
        '''Return len(self).
        '''
        return self.distances.nonnone()

    def __iter__(self) -> iter:
        '''Return iter(self).
        '''
        for ith in range(len(self.distances)):
            for jth in range(ith+1, len(self.distances)):
                if self.distances[ith, jth] is not None:
                    yield self.cities[ith], self.cities[jth]

    def remove_path_by_time_limit(self):
        '''Remove path by `time_limit`.

        Arguments:
        ==========
            None

        Returns:
        ========
            None
        '''
        for ith in range(self.city_number):
            for jth in range(ith+1, self.city_number):
                distance = self.distance_from_ith_jth(ith, jth)
                for airport in self.cities[ith].airports:
                    for aircraft in airport.aircrafts:
                        if aircraft is None:
                            break
                        time = distance/aircraft.speed*Time.MINUTE*Time.HOUR
                        if time < self.time_limit:
                            self.distances[ith, jth] = None
                            break
                    if self.distances[ith, jth] is None:
                        break

    def normalize_distances_by_distance_to_weights(self):
        '''Normalize `self.distances` by `distance_to_weights`.

        Arguments:
        ==========
            None

        Returns:
        ========
            None
        '''
        for ith in range(self.city_number):
            for jth in range(ith+1, self.city_number):
                if self.distances[ith, jth] is not None:
                    self.distances[ith, jth] = self.distance_to_weights(self.distances[ith, jth])


    def distance_from_ith_jth(self, ith:int, jth:int) -> float:
        '''Calculate the distance from `ith` city and `jth` city.

        Arguments:
        ==========
            ith: Integer
            jth: Integer

        Returns:
        ========
            Float
        '''
        assert all((0<=ith,jth<self.city_number)), 'Length Error'

        return self.cities[ith].distance_from(self.cities[jth])


class Symmetric:
    def __init__(self, length:int):
        '''Symmetric matrix with initial value zero.

        Arguments:
        ==========
            length: Integer

        Returns:
        ========
            None
        '''
        self.length = length
        self.value = [[0.0]*(i+1) for i in range(length)]

    def __repr__(self) -> str:
        '''Return repr(self).
        '''
        return '<SymmetricMatrix: ({0}x{0})>'.format(self.length)

    def __iter__(self) -> iter:
        '''Return iter(self).
        '''
        for row in self.value:
            for ele in row:
                yield ele

    def __len__(self) -> int:
        '''Return len(self).
        '''
        return self.length

    def __getitem__(self, index:[int, Tuple[int]]) -> float:
        '''Return self[index].
        '''
        assert isinstance(index, (int, Tuple)), 'Type Error'
        if isinstance(index, int):
            return self.__getitem__(self.idx_1d_to_2d(index))
        assert len(index)==2, 'Type Error'

        ith, jth = index
        if ith < jth:
            return self.__getitem__((jth, ith))
        return self.value[ith][jth]

    def __setitem__(self, index:[int, Tuple[int]], value:float):
        '''Set self[index] to value.
        '''
        assert isinstance(index, (int, Tuple)), 'Type Error'
        if isinstance(index, int):
            return self.__setitem__(self.idx_1d_to_2d(index), value)
        assert len(index)==2, 'Length Error'

        ith, jth = index
        if ith < jth:
            return self.__setitem__((jth, ith), value)
        self.value[ith][jth] = value

    @property
    def T(self) -> Airline:
        '''Transpose.'''
        return self

    @property
    def shape(self) -> Tuple[int]:
        '''Shape of `self`.'''
        return self.length, self.length

    def nonnone(self) -> int:
        '''Count the number of non-None elements.
        '''
        count = 0
        for value in self:
            if value is not None:
                count += 1
        return count

    def densify(self) -> np.matrix:
        '''Densify  the symmetric matrix.

        Arguments:
        ==========
            None

        Returns:
        ========
            numpy.matrix
        '''
        result = np.zeros((self.length, ) * 2)
        for ith in range(self.length):
            result[ith, ith] = self.value[ith][ith]
            for jth in range(ith+1, self.length):
                result[ith, jth] = self.value[jth][ith]
                result[jth, ith] = self.value[jth][ith]
        return result

    def idx_1d_to_2d(self, idx:int) -> Tuple[int]:
        '''Convert 1d `idx` to 2d.

        Arguments:
        ==========
            idx: Integer

        Returns:
        ========
            Tuple[Integer, Integer]
        '''
        row = idx % self.length
        col = idx // self.length
        return row, col



if __name__ == '__main__':
    from data import cities

    airline = Airline(cities, time_limit, distance_to_weights)
