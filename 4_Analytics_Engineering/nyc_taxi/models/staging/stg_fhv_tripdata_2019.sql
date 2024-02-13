select 
        {{dbt_utils.generate_surrogate_key(['dispatching_base_num', 'pickup_datetime'])}} as fhv_id,
        cast(dispatching_base_num as string) as dispatching_base_num ,
        cast(pickup_datetime as datetime) as pickup_datetime,
        cast(dropOff_datetime as datetime) as dropoff_datetime,
        cast(PUlocationID as int) as pu_location_id,
        cast(DOlocationID as int) as do_location_id,
        cast(SR_Flag as int) as sr_flag,
        cast(Affiliated_base_number as string) as affiliated_base_number
from {{ source('ny_taxi', 'fhv_tripdata_2019') }}