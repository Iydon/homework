-- What is the percentage of American films in all films in the 1970s. (The
-- result should be expressed percentage and approximated to 2 decimal places)
with target_movies as (
    select m.country, count(*) as cnt
    from movies as m
    where m.year_released between 1970 and 1979
    group by country
), number as (
    select sum(t.cnt)
    from target_movies as t
)
select round(100.0 * t.cnt / (select * from number), 2) as us_percent
from target_movies as t
where t.country = 'us';
