{{ config(materialized='table', schema='dev') }}

select
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4) as year,
    count(*) as beer_count
from {{ ref('beer_types') }}
where
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4) ~ '^\d{4}$'
group by year
order by year
