-- List the number of different actors who have been played in
-- the same movie with Yifei Liu (Yife herself is not included).
with lyf_id as (
    select p.peopleid
    from people as p
    where p.first_name = 'Yifei'
        and p.surname = 'Liu'
), lyf_movies as (
    select *
    from credits as c
    where c.peopleid = (select * from lyf_id)
)
select count(distinct c.peopleid) as 'count'
from lyf_movies as m
    join credits as c on c.movieid = m.movieid
        and c.credited_as = 'A'
where c.peopleid != (select * from lyf_id);
