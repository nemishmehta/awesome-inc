with monthly_installations as (
    select
        extract(month from installation_date) as month,
        count(*) as installations
    from
        {{ ref('fct_installation') }}
    group by month
)

select
    *
from
    monthly_installations