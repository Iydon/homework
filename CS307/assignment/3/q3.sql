select sub.district, sub.number, rank() over(order by sub.number desc)
from (
    select s.district, count(distinct ld.line_id) as number
    from line_detail as ld
        join stations as s on ld.station_id = s.station_id
    group by s.district
    having s.district != ''
) as sub;
