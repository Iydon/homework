-- How many actors have acted more than 30 movies.
select count(*) as cnt
from (
    select c.peopleid
    from credits as c
    where c.credited_as = 'A'
    group by c.peopleid
    having count(*) > 30
);
