

select
    type,
    count(beer_id) as count_beers
from (
    select
        beer_id,
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
    from "db"."dev"."raw_beer_data"
) as styles
group by type
order by count_beers desc