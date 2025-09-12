{{ config(
    materialized='table',
    schema='dev'
) }}

select
    beer_id,
    name,
    tagline,
    first_brewed,
    abv,
    ibu,
    ebc,
    ph,
    case
        when lower(tagline) like '%lager%' then 'Lager'
        when lower(tagline) like '%pilsner%' then 'Lager'
        when lower(tagline) like '%ipa%' then 'Ale'
        when lower(tagline) like '%stout%' then 'Ale'
        when lower(tagline) like '%porter%' then 'Ale'
        when lower(tagline) like '%ale%' then 'Ale'
        when lower(tagline) like '%wheat%' then 'Ale'
        else 'Other'
    end as type
from {{ source('dev', 'raw_beer_data') }}
