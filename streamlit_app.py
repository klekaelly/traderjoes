import streamlit as st
import pandas as pd
import os
from core import api_com, config, query
from df_controller import DataFrameHandler

st.title("NIS")

# Toggle for availability filter
availability_option = st.radio(
    "Show items that are:",
    options=["Available", "Not Available"],
    index=0
)
availability_value = "1" if availability_option == "Available" else "0"

# Ensure the queries directory is set to the current workspace
config.QUERIES_DIR = os.getcwd()

# Load the GraphQL query
query_str = query.load_query(config.get_path("get_new_items.graphql"))

# Fetch all pages of items
all_items = []
current_page = 1
max_pages = 5

while current_page <= max_pages:
    config.CURRENT_PAGE = current_page
    # Pass the availability variable to the API call
    response = api_com.fetch_data(query_str, variables={
        "pageSize": config.PAGE_SIZE,
        "currentPage": config.CURRENT_PAGE,
        "storeCode": config.STORE_ID,
        "published": "1",
        "availability": availability_value,
        "newProduct": "1"
    })
    data = response.get('data', {})
    if not data:
        break
    top_level_key = next(iter(data), None)
    if not top_level_key:
        break
    products = data[top_level_key]
    items = products.get('items', [])
    page_info = products.get('page_info', {})
    if not items:
        break
    all_items.extend(items)
    total_pages = page_info.get('total_pages', 1)
    if current_page >= total_pages:
        break
    current_page += 1

if all_items:
    df = pd.DataFrame(all_items)
    df = DataFrameHandler.post_process_dataframe(df)
    if 'first_published_date' in df.columns:
        df['first_published_date'] = pd.to_datetime(df['first_published_date']).dt.strftime('%m-%d-%Y')
    st.dataframe(df)
else:
    st.write("No new items found.")
