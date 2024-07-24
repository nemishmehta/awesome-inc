with int_dim_product as (
    select
        id,
        reference,
        name,
        category_id,
        cast(price as float) as price
    from
        {{ source('bronze', 'product') }}
)
select
    *
from
    int_dim_product