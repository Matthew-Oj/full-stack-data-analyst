import requests
import pandas as pd

# API endpoint for orders (example from Fake Store API)
api_url = "https://fakestoreapi.com/carts"

def fetch_orders():
    response = requests.get(api_url)
    response.raise_for_status()  # Raise error if request fails
    data = response.json()
    return data

def transform_orders(raw_data):
    # Flatten nested JSON into tabular format
    orders_list = []
    for order in raw_data:
        for item in order['products']:
            orders_list.append({
                'order_id': order['id'],
                'user_id': order['userId'],
                'product_id': item['productId'],
                'quantity': item['quantity']
            })
    df = pd.DataFrame(orders_list)
    return df

if __name__ == "__main__":
    raw_data = fetch_orders()
    df_orders = transform_orders(raw_data)
    print(df_orders.head())
    
    # Optional: Save as CSV for loading into your warehouse/dbt
    df_orders.to_csv("data/api_orders.csv", index=False)
