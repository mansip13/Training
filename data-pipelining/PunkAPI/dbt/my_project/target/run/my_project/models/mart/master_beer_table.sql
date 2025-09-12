
  
    

  create  table "db"."dev"."master_beer_table__dbt_tmp"
  
  
    as
  
  (
    

with beers as (
    select * from "db"."dev"."staging"
)

select
    beer_id,
    beer_name,
    tagline as category,         -- category/style approximation
    description,
    abv as alcohol_percent,
    first_brewed
from beers
  );
  