{{ config(
    materialized='table'
) }}

WITH latest AS (
    SELECT
        customer_id,
        customer_name,
        region,
        signup_date,
        last_updated,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY last_updated DESC
        ) AS row_num
    FROM 
        {{ source('sales', 'raw_customers') }}
)

SELECT 
    customer_id,
    customer_name,
    region,
    signup_date 
FROM 
    latest
WHERE 
    row_num = 1