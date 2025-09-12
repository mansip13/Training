
  
    

  create  table "db"."dev_dev"."beer_released__dbt_tmp"
  
  
    as
  
  (
    

select
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4) as year,
    count(*) as beer_count
from "db"."dev_dev"."beer_types"
where
    left(coalesce(nullif(trim(first_brewed),''), '0000'), 4) ~ '^\d{4}$'
group by year
order by year
  );
  