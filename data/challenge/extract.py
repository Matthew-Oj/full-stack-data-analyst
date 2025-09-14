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