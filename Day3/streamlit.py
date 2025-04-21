import streamlit as st
import pandas as pd
import io

# Title of the application
st.set_page_config(page_title="Script Generator", layout="wide")
st.title("Dataset Prediction Script Generator with Chatbot")

# Step 1: Upload Dataset
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel file)", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    # Check the file extension and read the dataset
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")
        st.stop()

    # Step 2: Display Dataset
    st.write("Uploaded Dataset:")
    st.write(df)

    # Step 3: Select Prediction Column
    st.write("Select the column to predict:")
    prediction_column = st.selectbox("Choose the target column", df.columns)

    # Step 4: Select Features (Input Columns)
    st.write("Select the features (input columns) for prediction:")
    feature_columns = st.multiselect("Choose the feature columns", df.columns)

    if prediction_column and feature_columns:
        # Step 5: Generate and Download Program
        st.write("Generate Python Script with Chatbot for Prediction:")

        # Generate a Python script with a chatbot and prediction logic
        script = f"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from transformers import pipeline

# Load the dataset
df = pd.read_{'csv' if uploaded_file.name.endswith('.csv') else 'excel'}('{uploaded_file.name}')

# Prepare the data for prediction
X = df[{feature_columns}]  # Features
y = df['{prediction_column}']  # Target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Initialize the chatbot (using a pre-trained NLP model)
chatbot = pipeline("text-generation", model="gpt-2")  # You can replace "gpt-2" with any other model

def predict_price(input_data):
    # Predict the price based on input data
    prediction = model.predict([input_data])
    return prediction[0]

def ask_question(question):
    # Generate a response using the chatbot
    response = chatbot(question, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

# Chatbot interaction loop
print("Chatbot is ready! Ask me anything about the data or request predictions.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break
    elif "predict" in user_input.lower():
        try:
            # Extract feature values from the user input
            feature_values = []
            for feature in {feature_columns}:
                value = float(input(f"Enter the value for {{feature}}: "))
                feature_values.append(value)

            # Predict the price
            predicted_price = predict_price(feature_values)
            print(f"Chatbot: The predicted {prediction_column} is ${{predicted_price:.2f}}")
        except Exception as e:
            print(f"Chatbot: Sorry, I couldn't process your request. Error: {{e}}")
    else:
        # General chatbot response
        answer = ask_question(user_input)
        print(f"Chatbot: {{answer}}")
"""

        # Display the script
        st.code(script, language='python')

        # Download the script
        script_bytes = script.encode('utf-8')
        script_io = io.BytesIO(script_bytes)
        st.download_button(
            label="Download Python Script with Chatbot",
            data=script_io,
            file_name="prediction_script_with_chatbot.py",
            mime="text/x-python"
        )
else:
    st.write("Please upload a CSV or Excel file and select the prediction column and features.")