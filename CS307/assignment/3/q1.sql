(
    select ld.station_id
    from line_detail as ld
    where ld.line_id = 1
) except (
    select ld.station_id
    from line_detail as ld
    where ld.line_id = 2
) order by station_id;
