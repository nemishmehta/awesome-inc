with int_dim_country as (
    select
        id,
        name,
        region,
        dbt_scd_id,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from
        {{ ref('country_snapshot') }}
)
select
    *
from
    int_dim_country