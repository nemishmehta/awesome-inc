with int_dim_customer as (
    select
        id,
        name,
        email,
        country_id,
        premium_customer
    from
        {{ source('bronze', 'customer') }}
)
select
    *
from
    int_dim_customer