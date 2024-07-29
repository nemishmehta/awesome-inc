{% snapshot customer_snapshot %}

{{
    config(
        target_database='awesomeinc',
        target_schema='warehouse',
        strategy='check',
        unique_key='id',
        check_cols=['name', 'email', 'country_id', 'premium_customer'],
    )
}}

select * from {{ source('bronze', 'customer') }}

{% endsnapshot %}