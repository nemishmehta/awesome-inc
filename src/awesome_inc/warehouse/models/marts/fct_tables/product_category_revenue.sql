with fct_installation as (
    select
        category_id,
        revenue
    from
        {{ ref('fct_installation') }}
),

dim_product_category as (
    select
        id,
        name as category_name
    from
        {{ ref('dim_product_category') }}
),

product_category_revenue as (
    select
        category_name,
        sum(revenue) as total_revenue
    from
        fct_installation
    left join
        dim_product_category
        on fct_installation.category_id = dim_product_category.id
    group by category_name
)

select
    *
from
    product_category_revenue