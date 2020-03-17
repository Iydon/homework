-- List all films made after 2000 (including 2000) with the
-- max number of actors borned after 2000 (including 2000)
with actors as (
    select m.movieid as movieid, count(*) as cnt
    from credits as c
        join people as p on p.peopleid = c.peopleid and p.born >= 2000
        join movies as m on m.movieid = c.movieid and m.year_released >= 2000
    group by m.movieid
    -- having cnt < 3
)
select a.movieid, a.cnt
from actors as a
where a.cnt = (select max(cnt) from actors);
