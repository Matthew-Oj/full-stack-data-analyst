{{ config(
    materialized='table'
) }}

-- Combine orders with customer info
WITH sales_with_customers AS (
    SELECT
        o.order_id,
        o.order_date,
        o.customer_id,
        c.customer_name,
        c.region,
        o.product,
        o.quantity,
        o.price,
        o.total_amount
    FROM 
        {{ ref('stg_orders') }} o
    LEFT JOIN 
        {{ ref('stg_customers') }} c
    ON 
        o.customer_id = c.customer_id
),

-- Aggregate insights (beginner/intermediate)
sales_aggregated AS (
    SELECT
        order_id,
        order_date,
        customer_id,
        customer_name,
        region,
        COUNT(DISTINCT product) AS num_products_ordered,   -- number of distinct products in order
        SUM(quantity) AS total_quantity,                  -- total items
        SUM(total_amount) AS total_order_amount           -- total value
    FROM 
        sales_with_customers
    GROUP BY
        order_id, order_date, customer_id, customer_name, region
)

SELECT *
FROM sales_aggregated
