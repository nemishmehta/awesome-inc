with int_dim_country as (
    select
        id,
        name,
        region
    from
        {{ source('bronze', 'country') }}
)
select
    *
from
    int_dim_country