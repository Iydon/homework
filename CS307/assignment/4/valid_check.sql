create or replace function is_id_valid(code varchar)
returns bool as $body$
declare
    address_code char(6);
    birthday_code char(8);
    checksum_code char(1);
    weights integer[];
    map char(1)[];
    total integer;
begin
    -- 判断 code 长度是否合法并赋值
    if (length(code) != 18) then
        raise exception 'error_code: 0x01';
    end if;
    address_code := substr(code, 1, 6);
    birthday_code := substr(code, 7, 8);
    checksum_code := substr(code, 18, 1);
    -- 判断 address_code 是否合法
    select count(*) from district as d where d.code = address_code limit 1 into total;
    if (total != 1) then
        raise exception 'error_code: 0x02';
    end if;
    -- 判断 birthday_code 是否合法
    begin
        if (to_timestamp(birthday_code, 'yyyyMMdd') < '1970-01-01'::date) then
            raise exception 'error_code: 0x03';
        end if;
    exception
        when others then raise exception 'error_code: 0x04';
    end;
    -- 判断 checksum_code 是否合法
    weights := array[7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];
    total := 0;
    for ith in 1 .. 17 loop
        total := total + weights[ith]*cast(substr(code, ith, 1) as integer);
    end loop;
    map := array['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];
    if (upper(checksum_code) != map[total%11+1]) then
        raise exception 'error_code: 0x05';
    end if;
    -- 返回值
    return true;
end;
$body$ language plpgsql;
