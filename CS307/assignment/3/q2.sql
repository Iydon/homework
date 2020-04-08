select sub.district, sub.number, rank() over(order by sub.number)
from (
    select s.district, count(*) as number
    from line_detail as ld
        join stations as s on ld.station_id = s.station_id
    where ld.line_id = 1
    group by s.district
) as sub;
