# -*- encode: utf-8 -*-
# cities -> airports -> aircrafts
import dill
import os
from typing import Tuple

from models import Context, Aircraft, Airport, City, Time
from model_airline import Airline, Symmetric
from settings import data_file, city_number, city_capacity, airport_capacity, aircraft_capacity, aircraft_speed, aircraft_capacity_ratio, people_number_ratio, \
    time_limit, distance_to_weights


def read_data(file:str) -> Tuple[Context, City, Time, Airline]:
    '''Read data from `file`.

    Arguments:
    ==========
        file: String

    Returns:
    ========
        Tuple[Context, City, Time, Airline]
    '''
    with open(file, 'rb') as f:
        return dill.load(f)

def write_data(file:str, context:Context, cities:City, airline:Airline, t:Time):
    '''Write date to `file`.

    Arguments:
    ==========
        file: String
        context: Context
        cities: City
        airline: Airline
        t: Time

    Returns:
    ========
        None
    '''
    with open(file, 'wb') as f:
        dill.dump((context, cities, airline, t), f)

def drop_data(file:str):
    '''Drop data from `file`.

    Arguments:
    ==========
        file: String

    Returns:
    ========
        None
    '''
    os.remove(file)


# Cache data
if os.path.exists(data_file):
    context, cities, airline, t = read_data(data_file)
else:
    context = Context()
    t = Time()
    cities = [City(city_capacity()) for i in range(city_number)]

    for city in cities:
        city.init_airport(airport_capacity, aircraft_capacity, aircraft_speed, aircraft_capacity_ratio, people_number_ratio)

    airline = Airline(cities, time_limit, distance_to_weights)

    write_data(data_file, context, cities, airline, t)
