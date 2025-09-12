

select
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4) as year,
    type,
    count(*) as beer_count
from "db"."dev_dev"."beer_types"
where
    -- Only keep non-null, non-empty years and ensure first 4 chars are digits
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4) ~ '^\d{4}$'
group by
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4),
    type
order by
    year,
    type