with fhv as 
(
    select *
    from {{ ref('stg_fhv_tripdata_2019') }}
),

zones as 
(
    select *
    from {{ ref('dim_zones') }}
)

select  fhv.*, 
        pickup.borough as pickup_borough,
        pickup.zone as pickup_zone,
        pickup.service_zone as pickup_service_zone,
        dropoff.borough as dropoff_borough,
        dropoff.zone as dropoff_zone,
        dropoff.service_zone as dropoff_service_zone
from fhv
inner join zones pickup 
on fhv.pu_location_id = pickup.locationid
inner join zones dropoff 
on fhv.pu_location_id = dropoff.locationid

