
  
    

  create  table "db"."dev"."weather_report__dbt_tmp"
  
  
    as
  
  (
    

select 
    city,
    temperature,
    weather_description,
    wind_speed,
    weather_time_local
from "db"."dev"."staging"
  );
  