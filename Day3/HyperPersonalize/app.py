from fastapi import FastAPI
import pandas as pd
import joblib
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from transformers import AutoModelForCausalLM, AutoTokenizer

from huggingface_hub import login
import requests
from together import Together

import os
os.environ["STREAMLIT_WATCH_SUPPORT"] = "false"

login("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")

# Load trained model and data
model = joblib.load("recommendation_model.pkl")
df = pd.read_csv("synthetic_time_series_spending_data_with_names.csv")

# Map categories to bank products
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

# Summarize customer spending
customer_spend = df.pivot_table(index=["Customer_ID", "Customer_Name"],
                                columns="Category", values="Daily_Spend", aggfunc="sum").fillna(0)

client = Together(api_key="tgp_v1_cKEclmBXjEfh_0p359F19ac6fUzUCPYKWzyakaZAALk")

app = FastAPI()


def generate_dynamic_response(customer_name, category):
    """Generate AI-based responses dynamically using LangChain"""
    customer_data = customer_spend.loc[customer_spend.index.get_level_values("Customer_Name") == customer_name]

    if customer_data.empty:
        return f"Sorry, {customer_name}. We don't have spending history for you."

    total_spend = customer_data[category].values[0] if category in customer_data else 0
    product = category_to_product.get(category, "a suitable bank product")

    prompt_template = PromptTemplate.from_template("""
    You are an AI banking assistant helping a customer with personalized spending insights.
    - Customer Name: {customer_name}
    - Spending Category: {category}
    - Total Spend: ${total_spend:.2f}
    - Recommended Product: {product}

    Generate a friendly and informative response suggesting how the customer can benefit from the recommended product.
    """)

    prompt = prompt_template.format(customer_name=customer_name, category=category, total_spend=total_spend,
                                    product=product)

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    ai_response = response.choices[0].message.content
    print(ai_response)

    return ai_response


@app.get("/recommend/")
def recommend(customer_name: str, category: str):
    """API endpoint to get AI-generated recommendations"""
    response = generate_dynamic_response(customer_name, category)
    return {"customer": customer_name, "category": category, "recommendation": response}

# Run using: uvicorn app:app --reload
