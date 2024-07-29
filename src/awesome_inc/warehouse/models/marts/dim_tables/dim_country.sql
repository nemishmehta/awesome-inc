with dim_country as (
    select
        *
    from
        {{ ref('stg_dim_country') }}
)
select
    *
from
    dim_country