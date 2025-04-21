import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

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

df = pd.read_csv("synthetic_time_series_spending_data_with_names.csv")

customer_spend = df.pivot_table(index=["Customer_ID", "Customer_Name", "Salary_Level"],
                                columns="Category", values="Daily_Spend", aggfunc="sum").fillna(0)


def recommend_product(row):
    top_category = row.idxmax()
    return category_to_product.get(top_category, "No_Specific_Product")


customer_spend["Recommended_Product"] = customer_spend.apply(recommend_product, axis=1)
customer_spend = customer_spend.reset_index()

X = customer_spend.drop(columns=["Customer_ID", "Customer_Name", "Salary_Level", "Recommended_Product"])
y = customer_spend["Recommended_Product"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, "recommendation_model.pkl")
print("✅ Model saved successfully!")

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")
