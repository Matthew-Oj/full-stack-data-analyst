{{ config(
    materialized='table'
) }}

SELECT
    order_id,
    order_date,
    customer_id,
    product,
    quantity,
    price,
    quantity * price AS total_amount
FROM 
    {{ source('sales', 'raw_orders') }}