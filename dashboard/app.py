import streamlit as st
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv
import os

# ---- Load environment variables and connect to Snowflake ----
@st.cache_data(ttl=300)
def load_data():
    load_dotenv()  # <-- Load credentials from .env

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


df = load_data()
st.dataframe(df)