import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# FastAPI endpoint
API_URL = "http://127.0.0.1:8000/recommend/"

st.set_page_config(page_title="Bank AI Assistant", page_icon="💳", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)



# Load the data with error handling
try:
    df = pd.read_csv("updates.csv")
except FileNotFoundError:
    st.error("File not found! Please ensure 'updates.csv' exists in the current directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

# Normalize column names to lowercase (optional)
df.columns = df.columns.str.lower()

# Check if 'date' column exists
if 'date' not in df.columns:
    st.error("The dataset does not contain a 'date' column. Please check the dataset.")
    st.stop()

# Convert date column to datetime format
try:
    df['date'] = pd.to_datetime(df['date'])
except Exception as e:
    st.error(f"Error converting 'date' column to datetime: {e}")
    st.stop()

# Sidebar for inputs
st.sidebar.header("Filters")
customer_name = st.sidebar.text_input("Enter Customer Name:")
category = st.sidebar.selectbox("Select spending category",
                        ["Groceries", "Dining", "Travel", "Shopping", "Entertainment", "Healthcare", "Utilities"])

# Bank product mapping
bank_products = {
    "Groceries_Card": ["Groceries"],
    "Dining_Cashback_Card": ["Dining"],
    "Travel_Reward_Card": ["Travel"],
    "Shopping_Discount_Card": ["Shopping", "Electronics"],
    "Entertainment_Card": ["Entertainment"],
    "Healthcare_Benefits_Card": ["Healthcare"],
    "Utility_Bill_Payment_Card": ["Utilities"]
}
category_to_product = {cat: product for product, cats in bank_products.items() for cat in cats}

# Header Section
st.title("💳 Bank AI Assistant")
st.write("Get personalized recommendations based on your spending!")

# Main App Logic
if customer_name:
    if customer_name not in df['customer_name'].unique():
        st.warning(f"No data found for customer '{customer_name}'. Please enter a valid customer name.")
        st.stop()

    # Filter data for the selected customer
    customer_data = df[df['customer_name'] == customer_name]

    if not customer_data.empty:
        # Group by category and calculate total spending
        spending_summary = customer_data.groupby("category")["daily_spend"].sum().reset_index()

        # Get top 5 spending categories
        top_5_spending = spending_summary.nlargest(5, "daily_spend")

        # Reset the index to make it sequential and start from 1
        top_5_spending = top_5_spending.reset_index(drop=True)
        top_5_spending.index = top_5_spending.index + 1  # Add 1 to start numbering from 1

        st.subheader("Top 5 Spending Categories")
        st.dataframe(top_5_spending)

        # Create a two-column layout for the main content
        col1, col2 = st.columns([3, 2])  # Adjust column widths for better use of space

        # Column 1: Top 5 Spending Categories and Bar Chart
        with col1:

            st.subheader("Spending Distribution (Bar Chart)")
            fig, ax = plt.subplots(figsize=(8, 5))  # Increase figure size for better visibility
            ax.bar(top_5_spending['category'], top_5_spending['daily_spend'], color='skyblue')
            plt.xlabel("Category")
            plt.ylabel("Total Spend")
            plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
            st.pyplot(fig)

        # Column 2: Pie Chart and Recommendations
        with col2:
            st.subheader("Spending Distribution (Pie Chart)")
            fig, ax = plt.subplots(figsize=(6, 5))  # Increase figure size for better visibility
            ax.pie(top_5_spending['daily_spend'], labels=top_5_spending['category'], autopct='%1.1f%%',
                   colors=['blue', 'green', 'red', 'purple', 'orange'])
            st.pyplot(fig)

        # Recommendations
        top_categories = top_5_spending['category'].tolist()
        recommended_products = [category_to_product.get(cat, "a suitable bank product") for cat in top_categories]

        st.subheader("Recommended Products")
        for i, product in enumerate(recommended_products):
            st.write(f"{i + 1}. For your spending in **{top_categories[i]}**, we recommend the **{product}**!")

        # Download Button (Centered at the bottom)
        st.markdown("---")

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


        # @st.cache_data
        # def convert_df_to_csv(dataframe):
        #     return dataframe.to_csv(index=False).encode('utf-8')
        #
        # csv = convert_df_to_csv(top_5_spending)
        # st.download_button(
        #     label="Download Top 5 Spending Categories as CSV",
        #     data=csv,
        #     file_name=f"{customer_name}_spending_summary.csv",
        #     mime="text/csv"
        # )
    else:
        st.warning("No spending data found for this customer.")