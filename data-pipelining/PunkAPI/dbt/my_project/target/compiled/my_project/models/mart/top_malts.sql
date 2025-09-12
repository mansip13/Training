

select
    malt_name,
    count(distinct beer_id) as beers_with_malt
from "db"."dev"."malt_ingredients"
where malt_name is not null
group by malt_name
order by beers_with_malt desc