import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px

import os
from dotenv import load_dotenv
import snowflake.connector


# ---- Snowflake connection ----
@st.cache_data(ttl=300)
def load_data():
    # Load environment variables from .env
    load_dotenv()

    conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
    
    query = "SELECT * FROM fct_sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---- Load data ----
st.title("Sales Dashboard")
df = load_data()

st.subheader("Sales Data Preview")
st.dataframe(df)

# ---- Metrics ----
total_orders = df['ORDER_ID'].nunique()
total_customers = df['CUSTOMER_ID'].nunique()
total_revenue = df['TOTAL_ORDER_AMOUNT'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Customers", total_customers)
col3.metric("Total Revenue", f"${total_revenue:,.2f}")

# ---- Visualizations ----
st.subheader("Revenue by Region")
fig_region = px.bar(
    df.groupby('REGION')['TOTAL_ORDER_AMOUNT'].sum().reset_index(),
    x='REGION', y='TOTAL_ORDER_AMOUNT', text='TOTAL_ORDER_AMOUNT',
    labels={'TOTAL_ORDER_AMOUNT':'Revenue'}, title="Revenue by Region"
)
st.plotly_chart(fig_region)

st.subheader("Orders Over Time")
df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'], format='%d/%m/%Y')
fig_time = px.line(
    df.groupby('ORDER_DATE')['TOTAL_ORDER_AMOUNT'].sum().reset_index(),
    x='ORDER_DATE', y='TOTAL_ORDER_AMOUNT',
    labels={'TOTAL_ORDER_AMOUNT':'Revenue'}, title="Revenue Over Time"
)
st.plotly_chart(fig_time)

st.subheader("Top Customers by Revenue")
top_customers = df.groupby('CUSTOMER_NAME')['TOTAL_ORDER_AMOUNT'].sum().reset_index().sort_values(by='TOTAL_ORDER_AMOUNT', ascending=False)
fig_customers = px.bar(top_customers, x='CUSTOMER_NAME', y='TOTAL_ORDER_AMOUNT', text='TOTAL_ORDER_AMOUNT', title="Top Customers by Revenue")
st.plotly_chart(fig_customers)
