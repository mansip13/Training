
  
    

  create  table "db"."dev"."staging__dbt_tmp"
  
  
    as
  
  (
    

with source as (
    select * 
    from "db"."dev"."raw_beer_data"
)

select 
    id,
    beer_id,
    name as beer_name,
    tagline,
    first_brewed,
    description,
    image,
    abv,
    ibu,
    ebc,
    ph,
    brewers_tips,
    contributed_by,
    inserted_at
from source
  );
  