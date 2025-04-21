import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/recommend/"

st.set_page_config(page_title="Bank AI Assistant", layout="centered")

st.title("💳 Bank AI Assistant")
st.write("Get personalized recommendations based on your spending!")

# User inputs
customer_name = st.text_input("Enter your name")
category = st.selectbox("Select spending category",
                        ["Groceries", "Dining", "Travel", "Shopping", "Entertainment", "Healthcare", "Utilities"])

if st.button("Get Offers"):
    if customer_name and category:
        params = {"customer_name": customer_name, "category": category}
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            st.success(response.json()["recommendation"])
        else:
            st.error("Failed to fetch recommendations. Try again!")
    else:
        st.warning("Please enter your name and select a category.")

