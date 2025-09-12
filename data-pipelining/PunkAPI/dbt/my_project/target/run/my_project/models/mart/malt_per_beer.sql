
  
    

  create  table "db"."dev_dev"."malt_per_beer__dbt_tmp"
  
  
    as
  
  (
    

select
    beer_id,
    malt_name as malt_type,
    amount_value as amount,
    amount_unit as unit
from "db"."dev"."malt_ingredients"
  );
  