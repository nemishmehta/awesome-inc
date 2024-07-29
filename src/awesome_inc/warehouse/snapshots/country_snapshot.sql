{% snapshot country_snapshot %}

{{
    config(
        target_database='awesomeinc',
        target_schema='warehouse',
        strategy='check',
        unique_key='id',
        check_cols=['name', 'region'],
    )
}}

select * from {{ source('bronze', 'country') }}

{% endsnapshot %}