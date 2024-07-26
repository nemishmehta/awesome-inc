with dim_product_category as (
    select
        *
    from
        {{ ref('stg_dim_product_category') }}
)
select
    *
from
    dim_product_category