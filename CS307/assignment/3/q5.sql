select sub.district, sub.chr, sub.cnt
from (
    select *, max(counter.cnt) over(partition by counter.district) as max
    from (
        select sub.district, sub.chr, count(*) as cnt
        from (
            select s.district, substr(s.chinese_name, 1, 1) as chr
            from stations as s
            where s.district != ''
        ) as sub
        group by sub.district, sub.chr
    ) as counter
) as sub
where sub.cnt = sub.max
order by sub.district asc, sub.chr asc;
