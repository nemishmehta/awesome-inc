with fct_installation as (
    select
        country_id,
        revenue
    from
        {{ ref('fct_installation') }}
),

dim_country as (
    select
        id,
        region
    from
        {{ ref('dim_country') }}
),

region_revenue as (
    select
        region,
        sum(revenue) as total_revenue
    from
        fct_installation
    left join
        dim_country
        on fct_installation.country_id = dim_country.id
    group by region
)

select
    *
from
    region_revenue