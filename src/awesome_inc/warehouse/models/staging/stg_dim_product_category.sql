with stg_dim_product_category as (
    select
        id,
        name,
        dbt_scd_id,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from
        {{ ref('product_category_snapshot') }}
)
select
    *
from
    stg_dim_product_category