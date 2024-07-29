with stg_fct_installation as (
    select
        id,
        name,
        description,
        product_id,
        customer_id,
        installation_date
    from
        {{ ref('stg_fct_installation') }}
),

dim_product as (
    select
        id,
        category_id,
        price as revenue
    from
        {{ ref('dim_product') }}
),

dim_customer as (
    select
        id,
        country_id
    from
        {{ ref('dim_customer') }}
),

fct_installation as (
    select
        stg_fct_installation.id,
        name,
        description,
        product_id,
        customer_id,
        installation_date,
        category_id,
        revenue,
        country_id
    from
        stg_fct_installation
        left join dim_product
            on stg_fct_installation.product_id = dim_product.id
        left join dim_customer
            on stg_fct_installation.customer_id = dim_customer.id
)

select
    *
from
    fct_installation

