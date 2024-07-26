with dim_product as (
    select
        *
    from
        {{ ref('stg_dim_product') }}
)
select
    *
from
    dim_product