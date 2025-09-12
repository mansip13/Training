
  
    

  create  table "db"."dev_dev"."abv_histogram__dbt_tmp"
  
  
    as
  
  (
    

select
    abv
from "db"."dev_dev"."beer_types"
where abv is not null
  );
  