{{ config(materialized='table', schema='dev') }}

select
    pairing,
    count(*) as pairing_count
from {{ source('dev', 'food_pairings') }}
where pairing is not null
group by pairing
order by pairing_count desc
