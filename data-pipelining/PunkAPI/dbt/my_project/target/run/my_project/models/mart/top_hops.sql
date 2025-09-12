
  
    

  create  table "db"."dev_dev"."top_hops__dbt_tmp"
  
  
    as
  
  (
    

select
    hop_name,
    count(distinct beer_id) as beers_with_hop
from "db"."dev"."hop_ingredients"
where hop_name is not null
group by hop_name
order by beers_with_hop desc
  );
  