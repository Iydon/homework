create or replace function insert_people()
returns trigger as $body$
declare
begin
    if (is_id_valid(new.id)) then
        new.birthday := substr(new.id, 7, 8);
        select string_agg(x.name, ',')
        from (
            select name from district as d
            where d.code in (
                substr(new.id, 1, 2) || '0000',
                substr(new.id, 1, 4) || '00',
                substr(new.id, 1, 6)
            )
        ) as x into new.address;
        return new;
    end if;
end;
$body$ language plpgsql;


create trigger people_trg
before insert on people
for each row when (new.id is not null)
    execute procedure insert_people();
