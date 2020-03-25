# -*- encode: utf-8 -*-
from configparser import ConfigParser


string = """
[IO]
ENCODE=utf-8

[DATA]
DIR=data
DAY=day.csv
HOUR=hour.csv
DATECOL=dteday
CASCOL=casual
REGCOL=registered
CNTCOL=cnt
INSCOL=instant
TIMECOL=["season", "yr", "mnth", "hr", "holiday", "weekday", "workingday"]
PLOTTIMECOL={"season":[1,4], "mnth":[1,12], "hr":[0,23], "workingday":[0,1]}
NOMCOL=["temp", "atemp", "hum", "windspeed"]

[TIME]
PATTERN=%%Y-%%m-%%d
"""

CFGS = ConfigParser()
CFGS.read_string(string)
