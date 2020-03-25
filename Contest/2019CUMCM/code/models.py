# -*- encode: utf-8 -*-
from decimal import Decimal
from faker import Faker
from math import radians, cos, sin, asin, sqrt
from typing import Callable, Iterable, List, Tuple, Dict

from settings import language, translation


faker = Faker(language)
faker.latlng = translation['latlng'][language]


# Phantom class
class Context: pass
class Aircraft: pass
class Airport: pass
class City: pass


class Context:
    def __init__(self):
        '''Initialize Context.

        Arguments:
        ==========
            None

        Returns:
        ========
            None
        '''
        self.dict = dict()

    def __getitem__(self, key:object) -> object:
        '''Return self[key].
        '''
        return self.dict.get(key)

    def __setitem__(self, key:object, value:object):
        '''Set self[key] to value.
        '''
        self.dict[key] = value

    def __repr__(self) -> str:
        '''Return repr(self).
        '''
        def not_start_end_with_(string:str, fix:str='_') -> bool:
            return not (string.startswith(fix) or string.endswith(fix))
        return str(list(filter(not_start_end_with_, dir(self))))


class Aircraft:
    def __init__(self, capacity:int, speed:int):
        '''Initialize Aircraft.

        Arguments:
        ==========
            capacity: Integer
            speed: Integer

        Returns:
        ========
            None
        '''
        self.capacity = capacity
        self.people_number = 0
        self.speed = speed

        self.name = faker.numerify('#'*9)

    def __repr__(self) -> str:
        '''Return repr(self).
        '''
        return '<Aircraft {} ({}/{})>'.format(self.name, self.people_number, self.capacity)

    def boarding(self, number:int=-1) -> bool:
        '''Boarding the aircraft.

        Arguments:
        ==========
            number: Integer

        Returns:
        ========
            Boolean
        '''
        if number > self.capacity-self.people_number:
            return False
        elif number < 0:
            self.people_number = self.capacity
        else:
            self.people_number += number
        return True

    def boarding_by_ratio(self, ratio:float) -> bool:
        '''Board the aircraft by ratio from 0 to 1.

        Arguments:
        ==========
            ratio: Float

        Returns:
        ========
            Boolean
        '''
        if not 0<ratio<1:
            return False
        return self.boarding(round(ratio*self.capacity))

    def disembarking(self, number:int=-1) -> bool:
        '''Disembarking the aircraft.

        Arguments:
        ==========
            number: Integer

        Returns:
        ========
            Boolean
        '''
        if number > self.people_number:
            return False
        elif number < 0:
            self.people_number = 0
        else:
            self.people_number -= number
        return True


class Airport:
    def __init__(self, capacity:int):
        '''Initialize Airport.

        Arguments:
        ==========
            capacity: Integer

        Returns:
        ========
            None
        '''
        if isinstance(capacity, Callable):
            print(capacity)
        self.capacity = capacity
        self.aircrafts = [None] * self.capacity
        self.aircraft_number = 0

        self.name = faker.city_name() + translation['airport'][language]

    def __repr__(self) -> str:
        '''Return repr(self).
        '''
        return '<Airport: {} ({}/{})>'.format(self.name, self.aircraft_number, self.capacity)

    def __iter__(self) -> iter:
        '''Return iter(self).
        '''
        for aircraft in self.aircrafts:
            if aircraft is not None:
                yield aircraft

    def init_coordinate(self, coordinate:Tuple[Decimal]):
        '''Initialize the coordinate of Airport.

        Arguments:
        ==========
            coordinate: Tuple[Decimal, Decimal]

        Returns:
        ========
            None
        '''
        assert len(coordinate)==2, 'Length Error'
        latitude = faker.coordinate(coordinate[0])
        longitude = faker.coordinate(coordinate[1])
        self.coordinate = (latitude, longitude)

    def init_aircraft(self, aircraft_capacity:Callable, aircraft_speed:Callable, aircraft_capacity_ratio:Callable, people_number_ratio:Callable):
        '''Initialize the aircraft of Airport.

        Arguments:
        ==========
            aircraft_capacity: Callable
            aircraft_speed: Callable
            aircraft_capacity_ratio: Callable
            people_number_ratio: Callable

        Returns:
        ========
            None
        '''
        assert isinstance(aircraft_capacity, Callable), 'Type Error'
        assert isinstance(aircraft_speed, Callable), 'Type Error'
        assert isinstance(aircraft_capacity_ratio, Callable), 'Type Error'
        assert isinstance(people_number_ratio, Callable), 'Type Error'

        for idx in range(round(aircraft_capacity_ratio()*self.capacity)):
            self.aircrafts[idx] = Aircraft(aircraft_capacity(), aircraft_speed())
            self.aircrafts[idx].boarding_by_ratio(people_number_ratio())
            self.aircraft_number += 1

    def aircraft_leave_for_times(self, airport:Airport, number:int=1) -> Dict[Aircraft, int]:
        '''Calculate the times of the aircrafts leaving for `airport`.

        Arguments:
        ==========
            airport: Airport
            number: Integer

        Returns:
        ========
            Dict[Aircraft, Integer]
        '''
        distance = self.distance_from(airport)
        out = self.aircraft_out(number)
        if airport.aircraft_in(out):
            times = [round(distance/o.speed*Time.HOUR*Time.MINUTE) for o in out]
            return dict(zip(out, times))
        return {}

    def aircraft_out(self, number:int=1) -> List[Aircraft]:
        '''Pop the aircrafts out from Airport.

        Arguments:
        ==========
            number: Integer

        Returns:
        ========
            List[Aircraft, ...]
        '''
        if number > self.aircraft_number:
            return []
        self.aircraft_number -= number
        result = [None] * number
        ith = 0
        for idx, aircraft in enumerate(self.aircrafts):
            if aircraft is not None:
                result[ith] = aircraft
                ith += 1
                self.aircrafts[idx] = None
                if ith >= number:
                    break
        return result

    def aircraft_in(self, aircrafts:List[Aircraft]) -> bool:
        '''Put the aircrafts into Airport.

        Arguments:
        ==========
            aircrafts: List[Aircraft, ...]

        Returns:
        ========
            Boolean
        '''
        length = len(aircrafts)
        if length > self.capacity-self.aircraft_number:
            return False
        self.aircraft_number += length
        ith = 0
        for idx, aircraft in enumerate(self.aircrafts):
            if aircraft is None:
                self.aircrafts[idx] = aircrafts[ith]
                ith += 1
                if ith >= length:
                    break
        return True

    def getattr_from_aircraft(self, key:str) -> list:
        '''Get the attribution from all of the aircrafts.

        Arguments:
        ==========
            key: String

        Returns:
        ========
            List[Object, ...]
        '''
        attrs = (getattr(aircraft, key, None) for aircraft in self.aircrafts)
        return list(filter(lambda x: x is not None, attrs))

    def distance_from(self, place:[Airport, City]) -> float:
        '''Calculate the distance between `self` and `place` (unit: km).

        Arguments:
        ==========
            place: [Airport, City]

        Returns:
        ========
            Float
        '''
        lat1, lon1 = map(radians, self.coordinate)
        lat2, lon2 = map(radians, place.coordinate)

        dlat, dlon = lat1-lat2, lon1-lon2
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return 2*asin(sqrt(a)) * 6371

    def filter(self, condition:Callable) -> iter:
        '''Filter iteration. Or filter(condition, self).
        '''
        for aircraft in self:
            if condition(aircraft):
                yield aircraft


class City:
    def __init__(self, capacity:int):
        '''Initialize the City.

        Arguments:
        ==========
            capacity: Integer

        Returns:
        ========
            None
        '''
        self.capacity = capacity
        self.airports = [None] * self.capacity

        self.name = faker.city()
        self.coordinate = faker.latlng()

    def __repr__(self) -> str:
        '''Return repr(self).
        '''
        return '<City: {} ({})>'.format(self.name, self.capacity)

    def init_airport(self, airport_capacity:[Iterable, Callable], aircraft_capacity:Callable, aircraft_speed:Callable, aircraft_capacity_ratio:Callable, people_number_ratio:Callable):
        '''Initialize the airports of City.

        Arguments:
        ==========
            airport_capacity: [Iterable, Callable]
            aircraft_capacity: Callable
            aircraft_speed: Callable
            aircraft_capacity_ratio: Callable
            people_number_ratio: Callable

        Returns:
        ========
            None
        '''
        assert isinstance(airport_capacity, (Iterable, Callable)), 'Type Error'
        assert isinstance(aircraft_capacity, Callable), 'Type Error'
        assert isinstance(aircraft_speed, Callable), 'Type Error'
        assert isinstance(aircraft_capacity_ratio, Callable), 'Type Error'
        assert isinstance(people_number_ratio, Callable), 'Type Error'
        if isinstance(airport_capacity, Iterable):
            assert len(airport_capacity)==self.capacity, 'Length Error'

        if isinstance(airport_capacity, Callable):
            airport_capacity = [airport_capacity() for idx in range(self.capacity)]
        airport_capacity = iter(airport_capacity)
        for idx in range(self.capacity):
            self.airports[idx] = Airport(next(airport_capacity))
            self.airports[idx].init_coordinate(self.coordinate)
            self.airports[idx].init_aircraft(aircraft_capacity, aircraft_speed, aircraft_capacity_ratio, people_number_ratio)

    def getattr_from_airport(self, key:str) -> list:
        '''Get the attribution from all of the airports.

        Arguments:
        ==========
            key: String

        Returns:
        ========
            List[Object, ...]
        '''
        attrs = (getattr(airport, key, None) for airport in self.airports)
        return list(filter(lambda x: x is not None, attrs))

    def distance_from(self, place:[Airport, City]) -> float:
        '''Calculate the distance between `self` and `place` (unit: km).

        Arguments:
        ==========
            place: [Airport, City]

        Returns:
        ========
            Float
        '''
        lat1, lon1 = map(radians, self.coordinate)
        lat2, lon2 = map(radians, place.coordinate)

        dlat, dlon = lat1-lat2, lon1-lon2
        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        return 2*asin(sqrt(a)) * 6371


class Time:
    MINUTE, HOUR, DAY, MONTH, YEAR = 60, 60, 24, 30, 12

    def __init__(self):
        '''Initialize the Time.

        Arguments:
        ==========
            None

        Returns:
        ========
            None
        '''
        self.now = 0
        self.day = (6, 0, 0), (18, 0, 0)
        self.dict = dict()

    def __repr__(self):
        '''Return repr(self)
        '''
        return '{}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}'.format(*self.ymdhms())

    def elapse(self, second:[int, Tuple[int]]=1):
        '''Time elapsed.

        Arguments:
        ==========
            second: [Integer, Tuple[Integer, ...]]

        Returns:
        ========
            None
        '''
        del_keys = []
        if not isinstance(second, int):
            second = self.to_second(second)
        self.now += second
        for key in self.dict:
            self.dict[key][0] -= second
            if self.dict[key][0] < 0:
                if isinstance(self.dict[key][1], Callable):
                    self.dict[key][1]()
                del_keys.append(key)
        for key in del_keys:
            del self.dict[key]

    def year_month_day_hour_minute_second(self) -> Tuple[int]:
        '''Convert the second (self.now) to (year, month, day, hour, minute, second).

        Arguments:
        ==========
            None

        Returns:
        ========
            Tuple[Integer, ...]
        '''
        now = self.now
        second = now % self.MINUTE
        now //= self.MINUTE
        minute = now % self.HOUR
        now //= self.HOUR
        hour = now % self.DAY
        now //= self.DAY
        day = now % self.MONTH
        now //= self.MONTH
        month = now % self.YEAR
        now //= self.YEAR
        year = now
        return year, month, day, hour, minute, second

    def ymdhms(self) -> Tuple[int]:
        '''Return self.year_month_day_hour_minute_second.
        '''
        return self.year_month_day_hour_minute_second()

    def to_second(self, value:Tuple[int]) -> int:
        '''Convert the (year, ..., second) to second.

        Arguments:
        ==========
            value: Tuple[Integer]

        Returns:
        ========
            Integer
        '''
        length = len(value)
        if length > 6:
            raise AssertionError('Length Error')
        elif length < 6:
            return self.to_second((0,)*(6-length)+value)

        para = 1
        paras = [self.MINUTE, self.HOUR, self.DAY, self.MONTH, self.YEAR]
        now = para * value[-1]
        for idx in range(len(paras)):
            para *= paras[idx]
            now += para * value[-idx-2]
        return now

    def is_day(self) -> bool:
        '''Whether it is daytime.

        Arguments:
        ==========
            None

        Returns:
        ========
            None
        '''
        _, _, _, h, m, s = self.ymdhms()
        now = self.to_second((h, m, s))
        day = self.to_second(self.day[0]), self.to_second(self.day[1])
        return day[0] < now < day[1]

    def is_night(self) -> bool:
        '''Whether it is night.

        Arguments:
        ==========
            None

        Returns:
        ========
            None
        '''
        return not self.is_day()

    def set_day(self, day:Tuple[Tuple]):
        '''Ste the rule of judging the daytime.

        Arguments:
        ==========
            day: Tuple[Tuple]

        Returns:
        ========
            None
        '''
        assert len(day)==2, 'Length Error'
        assert isinstance(day[0], Tuple), 'Type Error'
        assert isinstance(day[1], Tuple), 'Type Error'

        self.day = day

    def sleep(self, key:object, second:int=1, action:Callable=lambda:None):
        '''`key` sleeps for `second`.

        Arguments:
        ==========
            key: Object
            second: Integer
            action: Callable

        Returns:
        ========
            None
        '''
        self.dict.setdefault(key, [0, None])
        self.dict[key][0] += second
        self.dict[key][1] = action

    def is_active(self, key:object) -> bool:
        '''Whether `key` is active.

        Arguments:
        ==========
            key: Object

        Returns:
        ========
            Boolean
        '''
        return key not in self.dict
