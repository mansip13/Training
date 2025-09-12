

with beers as (
    select * from "db"."dev"."staging"
)

select
    count(*) as total_beers,
    round(avg(abv)::numeric, 2) as avg_abv,
    round(min(abv)::numeric, 2) as min_abv,
    round(max(abv)::numeric, 2) as max_abv,
    round(avg(ibu)::numeric, 2) as avg_ibu,
    round(min(ibu)::numeric, 2) as min_ibu,
    round(max(ibu)::numeric, 2) as max_ibu,
    round(avg(ebc)::numeric, 2) as avg_ebc,
    round(min(ebc)::numeric, 2) as min_ebc,
    round(max(ebc)::numeric, 2) as max_ebc,
    round(avg(ph)::numeric, 2) as avg_ph,
    min(first_brewed) as oldest_brew,
    max(first_brewed) as newest_brew,
    count(distinct contributed_by) as unique_contributors
from beers