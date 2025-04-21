import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define number of customers
num_customers = 10000  # 1 Lakh Customers
num_days = 365  # 1 Year of data

# Define salary levels and their impact on spending
salary_levels = {
    "Low": (500, 2000),     # Low-income spend range
    "Medium": (2000, 7000), # Medium-income spend range
    "High": (7000, 20000)   # High-income spend range
}

# Define spending categories
categories = ["Groceries", "Dining", "Travel", "Shopping", "Entertainment", "Healthcare", "Electronics", "Utilities"]

# Sample names list (can be extended)
first_names = ["John", "Alice", "Michael", "Emily", "David", "Sophia", "James", "Olivia", "Daniel", "Emma"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Martinez", "Lopez"]

# Generate random customer IDs, names, and assign salary levels
np.random.seed(42)  # For reproducibility
random.seed(42)

customer_ids = np.arange(1, num_customers + 1)
customer_names = [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(num_customers)]
salary_brackets = np.random.choice(["Low", "Medium", "High"], size=num_customers, p=[0.4, 0.4, 0.2])  # 40%-40%-20%

# Generate daily spending data
data = []

start_date = datetime(2024, 1, 1)
for customer, name, salary_level in zip(customer_ids, customer_names, salary_brackets):
    spend_range = salary_levels[salary_level]  # Get spending limits based on salary
    for day in range(num_days):
        date = start_date + timedelta(days=day)
        for category in categories:
            daily_spend = np.random.randint(spend_range[0], spend_range[1])  # Spending varies by salary
            data.append([customer, name, salary_level, date.strftime("%Y-%m-%d"), category, daily_spend])

# Create DataFrame
df = pd.DataFrame(data, columns=["Customer_ID", "Customer_Name", "Salary_Level", "Date", "Category", "Daily_Spend"])

# Save as CSV for analysis
df.to_csv("synthetic_time_series_spending_data_with_names.csv", index=False)

print(f"✅ Successfully generated daily spending data for {num_customers} customers over {num_days} days, including customer names.")
