

select
    pairing,
    count(*) as pairing_count
from "db"."dev"."food_pairings"
where pairing is not null
group by pairing
order by pairing_count desc