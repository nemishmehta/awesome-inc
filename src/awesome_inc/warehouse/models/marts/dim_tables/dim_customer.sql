with dim_customer as (
    select
        *
    from
        {{ ref('stg_dim_customer') }}
)
select
    *
from
    dim_customer