# 📊 Full-Stack Data Analyst Project

- [📊 Full-Stack Data Analyst Project](#-full-stack-data-analyst-project)
  - [Prerequisites](#prerequisites)
  - [Tech Stack](#tech-stack)
  - [Project Structure](#project-structure)
  - [Step-by-Step Guide](#step-by-step-guide)
    - [1. Clone Repo \& Install Python Dependencies](#1-clone-repo--install-python-dependencies)
    - [2. Database Setup (Snowflake)](#2-database-setup-snowflake)
      - [1. Create a Snowflake Trial Account](#1-create-a-snowflake-trial-account)
      - [2. Create a Warehouse, Database, and Schema](#2-create-a-warehouse-database-and-schema)
      - [3. Create a Role and Grant Permissions](#3-create-a-role-and-grant-permissions)
      - [4. Create a Table and Load CSV Data](#4-create-a-table-and-load-csv-data)
      - [5. dbt Setup - Local](#5-dbt-setup---local)
    - [3. Create Staging Models (Skeleton + Tasks)](#3-create-staging-models-skeleton--tasks)
    - [4. Create Mart Models (Skeleton + Tasks)](#4-create-mart-models-skeleton--tasks)
    - [5. Streamlit Dashboard (Snowflake)](#5-streamlit-dashboard-snowflake)
      - [1. Create a `.env` File](#1-create-a-env-file)
      - [2. Skeleton of a Streamlit App](#2-skeleton-of-a-streamlit-app)
      - [3. Task: Build Your Own Dashboard](#3-task-build-your-own-dashboard)
      - [4. Reflection Questions](#4-reflection-questions)
    - [6. Git \& GitHub](#6-git--github)
    - [7. Challenge Task: Load Data from Open API (Data Eng)](#7-challenge-task-load-data-from-open-api-data-eng)
      - [Open-Source API Suggestion](#open-source-api-suggestion)
      - [Skeleton for `extract.py`](#skeleton-for-extractpy)
      - [Task Instructions](#task-instructions)
  - [Learning Outcomes](#learning-outcomes)
  - [Questions or Issues?](#questions-or-issues)

---

An end-to-end beginner-friendly project to practice **data engineering + analytics** skills:

- Load raw **CSV data** into a **Snowflake database**  
- Transform the data with **dbt** into clean analysis-ready tables  
- Build a **Streamlit dashboard** for visualization  
- Use **Git + GitHub** for version control and collaboration  

---
## Prerequisites

Before starting this project, make sure you have the following installed or accounts ready:

* **Python 3.10+** – [Download Python](https://www.python.org/downloads/)
* **pip** (Python package manager) – comes with Python
* **Snowflake account** – [Sign up for free trial](https://signup.snowflake.com/)
* **dbt** – [Install dbt](https://docs.getdbt.com/docs/installation)
* **Streamlit** – [Install Streamlit](https://docs.streamlit.io/library/get-started/installation)
* **Git** – [Install Git](https://git-scm.com/downloads)
* **GitHub account** – [Sign up](https://github.com/join)
* **VS Code** – [Download Visual Studio Code](https://code.visualstudio.com/download)

---

## Tech Stack

* **Database**: Snowflake
* **Transformations**: dbt (data build tool)
* **Dashboard**: Streamlit
* **Version Control**: Git & GitHub

---

## Project Structure
```
full-stack-data-analyst/
│── data/                     # CSV files (raw input)
│   └── customers.csv
│   └── orders.csv
│
│── dbt_sales/                # dbt project folder - does not exist yet
│   ├── models/               # recommneded structure 
│   │   ├── staging/
│   │   │   └── stg_customers.sql
│   │   │   └── stg_orders.sql
│   │   ├── marts/
│   │   │   └── fct_sales.sql
│   │   └── schema.yml
│
│── dashboard/                # Streamlit app
│   └── .env
│   └── app.py
│
│── sql/                      # Optional raw SQL queries - empty
│   └── create_tables.sql
│
│── .gitignore
│── README.md
│── CONTRIBUTING.md
│── CODE_OF_CONDUCT.md
│── LICENSE
│── SECURITY.md
│── requirements.txt
```

---

## Step-by-Step Guide

### 1. Clone Repo & Install Python Dependencies

Clone the repository to your local machine using HTTPS:

```bash
git clone https://github.com/Matthew-Oj/full-stack-data-analyst.git
```

Navigate into the project folder:

```bash
cd full-stack-data-analyst
```


Install the required Python packages listed in requirements.txt:

```bash
pip install -r requirements.txt
```

Explanation:

The requirements.txt file contains a list of all Python packages needed for the project (e.g., pandas, dbt, streamlit, snowflake-connector-python, requests).

Running pip install -r requirements.txt automatically installs all these packages in your environment, ensuring the project runs smoothly without missing dependencies.

**Challenge - use a python virtual environment to isolate the packages!**

---

### 2. Database Setup (Snowflake)

#### 1. Create a Snowflake Trial Account
1. Go to [Snowflake Free Trial](https://signup.snowflake.com/).
2. Sign up with your email and choose a cloud provider (AWS, GCP, or Azure).
3. Log in to the Snowflake web UI (Snowsight).
---

#### 2. Create a Warehouse, Database, and Schema
In the Snowflake worksheet, run the following SQL:

```sql
-- Create a virtual warehouse (compute resource)
CREATE OR REPLACE WAREHOUSE sales_wh
  WITH WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

-- Create a database
CREATE OR REPLACE DATABASE sales_db;

-- Create a schema
CREATE OR REPLACE SCHEMA sales_schema;
```

---

#### 3. Create a Role and Grant Permissions

It’s best practice to use roles for security and access control:

```sql
-- Create a custom role
CREATE OR REPLACE ROLE analyst_role;

-- Grant usage on warehouse, database, and schema
GRANT USAGE ON WAREHOUSE demo_wh TO ROLE analyst_role;
GRANT USAGE ON DATABASE sales_db TO ROLE analyst_role;
GRANT USAGE ON SCHEMA sales_db.sales_schema TO ROLE analyst_role;

-- Allow creating tables
GRANT CREATE TABLE ON SCHEMA sales_db.sales_schema TO ROLE analyst_role;

-- Assign role to your user
GRANT ROLE analyst_role TO USER <your_username>;
```

---

#### 4. Create a Table and Load CSV Data
Create the two raw tables in your Snowflake database:

1. Customers table 

```sql
CREATE OR REPLACE TABLE sales_db.sales_schema.raw_customers (
    customer_id INT,
    customer_name VARCHAR,
    region VARCHAR,
    signup_date DATE,
    last_updated DATE
);
```
2. Orders table

```sql
CREATE OR REPLACE TABLE sales_db.sales_schema.raw_orders (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    product STRING,
    quantity INT,
    price NUMERIC(10,2)
);
```


Load CSV Data via Snowflake Web UI

   1. Open your Snowflake account and navigate to the left side pane Data → Database → SALES_DB → SALES_SCHEMA → Tables section 
   2. Select the table you want to load data into (e.g., raw_customers).
   3. Click Load Data (top right) → Upload File.
   4. Choose your CSV file (customers.csv or orders.csv).
   5. Map the CSV columns to the table columns (Snowflake usually auto-detects).
   6. Click Load to import the data.

---

#### 5. dbt Setup - Local

Step 1 - Install dbt

In VS Code open your terminal install dbt locally (via pip)
```bash
pip install -r requirements.txt
or 
pip install dbt-snowflake
```

---

Step 2 - Initialize the dbt Project

Run the following command in your terminal:

```bash
dbt init dbt_sales
```

This will:

* Create a folder called `dbt_sales/`
* Generate default dbt directories (`models/`, `tests/`, etc.)
* Prompt you to configure your connection (`profiles.yml`) interactively

---

Step 3 - Interactive Prompts

After running `dbt init`, dbt will ask you a series of questions. Here’s a guide for what to enter:

| Prompt                  | What to enter / guidance                                                             |
| ----------------------- | ------------------------------------------------------------------------------------ |
| **Project name**        | `dbt_sales` (letters, numbers, underscores only)                                     |
| **Database adapter**    | `1` for Snowflake                                                                    |
| **Account**             | Enter your Snowflake account identifier from the URL (e.g., `ab12345.eu-west-2.aws`) |
| **Username**            | Your Snowflake username (`FNAMELNAME123`)                                             |
| **Authentication type** | `1` for password (or keypair/SSO if configured)                                      |
| **Password**            | Your Snowflake password                                                              |
| **Role**                | The role you created (`analyst_role`)                                                |
| **Warehouse**           | Your warehouse (`SALES_WH`)                                                           |
| **Database**            | The database you created (`SALES_DB`)                                                |
| **Schema**              | The schema you created (`SALES_SCHEMA`)                                              |
| **Threads**             | How many threads dbt should use for parallel execution (e.g., `4`)                   |

💡 **Tip:** dbt will automatically write these settings into `~/.dbt/profiles.yml`. You can always edit this file manually later.

---

Step 4 - Verify the Connection

Once completed, run:

```bash
dbt debug
```

You should see:

```
Connection test: OK connection ok
```

✅ This confirms your Snowflake credentials are correctly set up and dbt can connect.

Optional step - Configure dbt Profile for Snowflake 
If using the **CLI**, create a `profiles.yml` file (usually in `~/.dbt/`):

```yaml
snowflake_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your_account>       # e.g. ab12345.eu-west-2.aws
      user: <your_username>
      password: <your_password>
      role: analyst_role
      database: SALES_DB
      warehouse: SALES_WH
      schema: SALES_SCHEMA
      threads: 4
      client_session_keep_alive: False
```

Replace `<your_account>`, `<your_username>`, and `<your_password>` with your Snowflake details.

---

Step 5 - Declare Sources
Inside `dbt/models/schema.yml`, declare the **raw tables**:

```yaml
version: 2

sources:
  - name: sales
    database: SALES_DB
    schema: SALES_SCHEMA
    tables:
      - name: raw_customers
      - name: raw_orders
```

Why this is done:

- It allows dbt to track lineage (which models depend on which raw tables).

- You can reference raw tables in models using {{ source('sales', 'raw_customers') }} instead of hardcoding table names.

- Makes your project modular, maintainable, and testable.

---

### 3. Create Staging Models (Skeleton + Tasks)

Staging models standardize column names and apply simple transformations.

Instead of full SQL, here’s a skeleton to guide you:

```sql
{{ config(
    materialized='table'  -- decide table, view, or incremental
) }}

SELECT
    -- list of columns from the source
FROM
    {{ source('your_source_name', 'your_raw_table') }}
WHERE
    -- optional filter
```

---

**Task 1: Create `stg_customers` in `models/staging/`**

Use the skeleton above to create a staging model for `raw_customers`.

Include a row number to get the latest record per customer:

```sql
ROW_NUMBER() OVER (
    PARTITION BY customer_id
    ORDER BY last_updated DESC
) AS row_num
```

Filter to only include the latest row per customer.

**Questions to answer after completing the task:**

* What columns from `raw_customers` did you include and why?
* Why is it important to only keep the latest record per customer?
* How does `materialized='table'` affect Snowflake storage?

---

**Task 2: Create `stg_orders` in `models/staging/`**

Create a staging model for `raw_orders`.

Calculate a new column `total_amount = quantity * price`.

**Questions:**

* Which columns should you keep from `raw_orders`?
* Why might you calculate `total_amount` in the staging model instead of in the mart?
* What materialization strategy would you choose for large datasets?

---

### 4. Create Mart Models (Skeleton + Tasks)

Mart models aggregate data for analysis. Skeleton:

```sql
{{ config(
    materialized='table'  -- you can also try view or incremental
) }}

WITH base AS (
    SELECT
        -- columns from staging models
    FROM
        {{ ref('stg_model_name') }}
    JOIN
        {{ ref('another_stg_model') }}
    ON
        -- join condition
),

aggregated AS (
    SELECT
        -- aggregated columns
    FROM
        base
    GROUP BY
        -- grouping columns
)

SELECT *
FROM aggregated
```

---

**Task 3: Create `fct_sales` in `models/marts/`**

* Join `stg_orders` with `stg_customers`.
* Aggregate at the order level:

  * Count distinct products
  * Sum quantity
  * Sum total amount

**Questions:**

* Which columns are necessary for reporting?
* Why is it useful to aggregate at the order level first?
* What materialization strategy is most efficient for your mart?

---

This approach gives learners a template + guided tasks, encouraging them to build the models themselves while reflecting on design decisions.


### 5. Streamlit Dashboard (Snowflake)

You will build a dashboard that connects to Snowflake, loads your `fct_sales` data, and visualizes it interactively.

---

#### 1. Create a `.env` File

Store your Snowflake credentials securely:

```env
# .env file for Snowflake connection
# dashboard/.env

SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=SALES_WH
SNOWFLAKE_DATABASE=SALES_DB
SNOWFLAKE_SCHEMA=SALES_SCHEMA
```

> **Tip:** Never commit your `.env` file to GitHub. Add it to `.gitignore`. For this project we have added it in for you.

---

#### 2. Skeleton of a Streamlit App

Here’s a **template** to get started:

```python
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
```

**Key point:** Using `load_dotenv()` and `os.getenv()` keeps your credentials secure and avoids hardcoding them.

---

#### 3. Task: Build Your Own Dashboard

1. Use the skeleton above to **load your Snowflake data**.
2. Add metrics using `st.metric()`. Example:

```python
total_orders = df['ORDER_ID'].nunique()
total_customers = df['CUSTOMER_ID'].nunique()
total_revenue = df['TOTAL_ORDER_AMOUNT'].sum()
```

3. Create visualizations using **Streamlit charts** or **Plotly**:

* Revenue by Region
* Orders Over Time
* Top Customers by Revenue

4. **Free exploration:** This is your opportunity to be creative—produce **any visualizations you like** using `df`.

---

#### 4. Reflection Questions

* How does loading variables via `.env` improve security?
* Why is caching (`@st.cache_data`) useful for dashboard performance?
* Which metrics or visualizations would help business stakeholders make decisions?


### 6. Git & GitHub

If you are starting from my repository, first **clone it**:

```bash
git clone https://github.com/Matthew-Oj/full-stack-data-analyst.git
cd full-stack-data-analyst
```

Now, if you want to push this project to **your own GitHub account**, do the following:

1. Create a new repository on your GitHub account (e.g., `full-stack-data-analyst`).
2. Change the remote URL to point to your repository:

```bash
git remote set-url origin https://github.com/<your-username>/full-stack-data-analyst.git
```

3. Verify the new remote:

```bash
git remote -v
```

You should see your repository URL for both fetch and push.

4. Commit any changes and push to your repository:

```bash
git add .
git commit -m "initial commit"
git push -u origin main
```

After this, your local copy is connected to your GitHub repo, and you can continue making commits and pushes as usual.

---

### 7. Challenge Task: Load Data from Open API (Data Eng)

This task is a **challenge** for learners to practice data ingestion from an external API into your project. You can find the starter skeleton here:

`data/challenge/extract.py`

---

#### Open-Source API Suggestion

* **Fake Store API** – free REST API with products, customers, and orders: [https://fakestoreapi.com/](https://fakestoreapi.com/)

---

#### Skeleton for `extract.py`

```python
import requests
import pandas as pd

# TODO: Replace with your API endpoint
API_URL = "https://fakestoreapi.com/carts"

# Function to fetch data from API
def fetch_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

# Function to transform API data into a DataFrame
def transform_data(raw_data):
    # TODO: Flatten JSON into table format
    df = pd.DataFrame()
    return df

# Optional: Save as CSV
if __name__ == "__main__":
    raw_data = fetch_data()
    df = transform_data(raw_data)
    df.to_csv("data/api_orders.csv", index=False)
```

---

#### Task Instructions

1. Use the skeleton in `data/challenge/extract.py`.
2. Connect to the Fake Store API.
3. Transform nested JSON into a flat table with columns like `order_id`, `user_id`, `product_id`, `quantity`.
4. Save the transformed data to `data/api_orders.csv`.
5. Optionally, load it into your Snowflake `raw_orders` table.

💡 **Tip:** This is a great opportunity to practice real-world data extraction and transformation. You can extend this to automate with Airflow or schedule recurring loads.


---

## Learning Outcomes
By completing this project, you will learn how to:
1. Ingest raw CSV data into Snowflake  
2. Transform data with dbt into analytics-friendly models  
3. Build a simple analytics dashboard  
4. Manage code with Git + GitHub  

---
## Questions or Issues?

Open an issue in this repo or reach out to:
- **Matthew Oj** – [edafeoj@gmail.com](mailto:edafeoj@gmail.com)

See example-solution for inspo