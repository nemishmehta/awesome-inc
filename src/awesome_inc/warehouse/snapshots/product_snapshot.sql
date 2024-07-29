{% snapshot product_snapshot %}

{{
    config(
        target_database='awesomeinc',
        target_schema='warehouse',
        strategy='check',
        unique_key='id',
        check_cols=['reference', 'name', 'category_id', 'price'],
    )
}}

select * from {{ source('bronze', 'product') }}

{% endsnapshot %}