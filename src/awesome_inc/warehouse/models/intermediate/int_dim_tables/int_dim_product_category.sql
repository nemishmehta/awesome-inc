with int_dim_product_category as (
    select
        id,
        name
    from
        {{ source('bronze', 'product_category') }}
)
select
    *
from
    int_dim_product_category