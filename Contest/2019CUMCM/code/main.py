# -*- encode: utf-8 -*-
from random import random, choice, choices
from tqdm import tqdm

from models import Context, Aircraft, Airport, City, Time
from data import context, cities, airline, t
from settings import randbool, randgauss, path_number, aircraft_number, people_number_ratio


population = {}
for city in cities:
    for airport in city.airports:
        population[airport] = [0] * t.DAY*t.HOUR*t.MINUTE


for i in tqdm(range(t.DAY*t.HOUR*t.MINUTE), ascii=True):
# for i in range(t.DAY*t.HOUR*t.MINUTE):
    t.elapse()

    paths = choices(list(airline), k=path_number(t.is_day()))
    for path in paths:
        aircrafts = []

        if randbool(): path=path[::-1]
        number = aircraft_number(t.is_day())
        path_ = choice(path[0].airports), choice(path[1].airports)

        if (len(list(path_[0].filter(t.is_active))) >= number) \
            and (path_[1].capacity-path_[1].aircraft_number > number) \
            and number != 0:
            times = path_[0].aircraft_leave_for_times(path_[1], number)
            for key, val in times.items():
                aircrafts.append(key)
                t.sleep(key, val)

        for aircraft in aircrafts:
            population[path_[1]][i] = round(people_number_ratio() * aircraft.capacity)
