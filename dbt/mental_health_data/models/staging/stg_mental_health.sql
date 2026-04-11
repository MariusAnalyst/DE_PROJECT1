with source as (

    select * from {{ source('raw_mental_health', 'mental_health_data') }}

)

select * from source
