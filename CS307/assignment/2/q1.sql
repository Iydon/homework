-- List the non-US movies released in 1991 and with titles begin with "The" .
select m.title, m.country, m.year_released
from movies as m
where m.country != 'us'
    and m.year_released = 1991
    and upper(m.title) like 'THE%';
