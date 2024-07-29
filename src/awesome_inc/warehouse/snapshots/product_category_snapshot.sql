{% snapshot product_category_snapshot %}

{{
    config(
        target_database='awesomeinc',
        target_schema='warehouse',
        strategy='check',
        unique_key='id',
        check_cols=['name'],
    )
}}

select * from {{ source('bronze', 'product_category') }}

{% endsnapshot %}