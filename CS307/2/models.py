from sqlalchemy import Column, ForeignKey, Integer, Sequence, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Country(Base):
    '''
    create table countries (
        country_code char(2) not null
            constraint countries_pkey
            primary key,
        country_name varchar(50) not null
            constraint countries_country_name_key
            unique,
        continent varchar(20) not null
    )
    '''
    __tablename__ = 'countries'

    country_code = Column(String(2), nullable=False, primary_key=True)
    country_name = Column(String(50), nullable=False, unique=True)
    continent = Column(String(20), nullable=False)


class Movie(Base):
    '''
    create table movies (
        movieid serial not null
            constraint movies_pkey
            primary key,
        title varchar(200) not null,
        country char(2) not null
            constraint movies_country_fkey
            references countries,
        year_released integer not null,
        runtime integer,
        constraint movies_title_country_year_released_key
            unique (title, country, year_released)
    )
    '''
    __tablename__ = 'movies'

    id = Column(Integer, Sequence('movie_id_seq'), nullable=False, primary_key=True)
    title = Column(String(200), nullable=False)
    country = Column(String(2), nullable=False)
    year_released = Column(Integer, nullable=False)
    runtime = Column(Integer)
