with int_fct_installation as (
    select
        id,
        name,
        description,
        product_id,
        customer_id,
        installation_date
    from
        {{ source('bronze', 'installation') }}
)
select
    *
from
    int_fct_installation