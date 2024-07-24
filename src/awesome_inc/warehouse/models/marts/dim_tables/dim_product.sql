with dim_product as (
    select
        *
    from
        {{ ref('int_dim_product') }}
)
select
    *
from
    dim_product