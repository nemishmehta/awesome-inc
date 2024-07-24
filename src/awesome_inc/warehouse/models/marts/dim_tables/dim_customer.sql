with dim_customer as (
    select
        *
    from
        {{ ref('int_dim_customer') }}
)
select
    *
from
    dim_customer