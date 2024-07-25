with int_dim_product as (
    select
        id,
        reference,
        name,
        category_id,
        cast(price as float) as price,
        dbt_scd_id,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from
        {{ ref('product_snapshot') }}
)
select
    *
from
    int_dim_product