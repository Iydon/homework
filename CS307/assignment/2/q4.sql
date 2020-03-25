-- List the names of the known directors of 2016 films by ascending order (no need to display
-- anything about the film). The film only from following regions: kr, hk, gb, ph. If the film is
-- Korean(kr) or HONG KONG(hk), the name should be displayed as surname followed by first
-- name, otherwise it must be first name followed by surname.
select (
    case
        when m.country in ('kr', 'hk') then
            coalesce(p.surname, ' ') || ' ' || p.first_name
        else
            coalesce(p.first_name, ' ') || ' ' || p.surname
    end
) as director
from credits as c
    join movies as m on c.movieid = m.movieid
    join people as p on c.peopleid = p.peopleid and c.credited_as = 'D'
where m.year_released = 2016
    and m.country in ('kr', 'hk', 'gb', 'ph')
order by director;
