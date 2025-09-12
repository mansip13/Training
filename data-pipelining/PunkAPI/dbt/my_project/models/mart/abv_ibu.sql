{{ config(materialized='table', schema='dev') }}

select
    abv,
    ibu,
    type
from {{ ref('beer_types') }}
where abv is not null and ibu is not null
