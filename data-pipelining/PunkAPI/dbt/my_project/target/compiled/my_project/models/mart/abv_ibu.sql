

select
    abv,
    ibu,
    type
from "db"."dev_dev"."beer_types"
where abv is not null and ibu is not null