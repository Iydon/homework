select ld.line_id, ld.station_id as station, sub.number,
    rank() over(partition by ld.line_id order by sub.number desc) as rank
from (
    select bl.station_id, count(bl.bus_line) as number
    from bus_lines as bl
    group by bl.station_id
    having count(bl.bus_line) >= 10
) as sub
    join line_detail as ld on ld.station_id = sub.station_id
order by ld.line_id, sub.number desc
limit 10 offset 15;
