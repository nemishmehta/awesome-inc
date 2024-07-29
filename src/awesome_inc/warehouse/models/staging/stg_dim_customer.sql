with stg_dim_customer as (
    select
        id,
        name,
        email,
        country_id,
        cast(premium_customer as boolean) as premium_customer,
        dbt_scd_id,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from
        {{ ref('customer_snapshot') }}
)
select
    *
from
    stg_dim_customer