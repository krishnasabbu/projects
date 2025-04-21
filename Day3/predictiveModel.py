import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error

# Function to handle missing values
def handle_missing_values(df, column, method):
    if method == 'Mean':
        df[column].fillna(df[column].mean(), inplace=True)
    elif method == 'Median':
        df[column].fillna(df[column].median(), inplace=True)
    elif method == 'Mode':
        mode_value = df[column].mode()
        if not mode_value.empty:
            df[column].fillna(mode_value[0], inplace=True)  # Use the first mode value
        else:
            df[column].fillna(df[column].iloc[0], inplace=True)  # Fallback to the first value
    return df

# Function to remove outliers using IQR
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Streamlit app
st.set_page_config(page_title="Predictive Model", page_icon=":bar_chart:", layout="wide")
st.title("Predictive Model Pipe Line")

# Initialize session state variables
if "step" not in st.session_state:
    st.session_state.step = 1
if "df" not in st.session_state:
    st.session_state.df = None
if "target_variable" not in st.session_state:
    st.session_state.target_variable = None
if "df_scaled" not in st.session_state:
    st.session_state.df_scaled = None
if "selected_features" not in st.session_state:
    st.session_state.selected_features = []
if "scaling_method" not in st.session_state:
    st.session_state.scaling_method = 'None'  # Default value for scaling method
if "model_type" not in st.session_state:
    st.session_state.model_type = 'Linear Regression'  # Default model type
if "missing_value_methods" not in st.session_state:
    st.session_state.missing_value_methods = {}  # Store imputation methods
if "outlier_columns" not in st.session_state:
    st.session_state.outlier_columns = []  # Store columns for outlier removal

# Sidebar with steps
st.sidebar.write("### Steps")
steps = [
    "Step 1: Upload Dataset",
    "Step 2: Select Target Variable",
    "Step 3: Handle Missing Values",
    "Step 4: S & N",
    "Step 5: Remove Outliers",
    "Step 6: Feature Selection",
    "Step 7: Model Selection",
    "Step 8: Generate Python Code"
]

# Create buttons for each step in the sidebar
step_buttons = {}
for idx, step in enumerate(steps, start=1):
    step_buttons[step] = st.sidebar.button(step, key=idx)

# Update session state based on button clicks
if step_buttons[steps[0]]:
    st.session_state.step = 1
elif step_buttons[steps[1]]:
    st.session_state.step = 2
elif step_buttons[steps[2]]:
    st.session_state.step = 3
elif step_buttons[steps[3]]:
    st.session_state.step = 4
elif step_buttons[steps[4]]:
    st.session_state.step = 5
elif step_buttons[steps[5]]:
    st.session_state.step = 6
elif step_buttons[steps[6]]:
    st.session_state.step = 7
elif step_buttons[steps[7]]:
    st.session_state.step = 8

# Main content for the selected step
if st.session_state.step == 1:
    st.write("### Step 1: Upload Dataset")
    uploaded_file = st.file_uploader("Upload your dataset (CSV file)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df
        st.write("Uploaded Dataset:")
        st.write(df)

if st.session_state.step == 2:
    st.write("### Step 2: Select Target Variable")
    if st.session_state.df is not None:
        df = st.session_state.df
        target_variable = st.selectbox(
            "Select the target variable", df.columns,
            index=df.columns.get_loc(st.session_state.target_variable) if st.session_state.target_variable else 0
        )
        st.session_state.target_variable = target_variable
        st.write(f"Selected target variable: {target_variable}")

if st.session_state.step == 3:
    st.write("### Step 3: Handle Missing Values")
    if st.session_state.df is not None:
        df = st.session_state.df
        missing_columns = df.columns[df.isnull().any()].tolist()
        if missing_columns:
            st.write("The following columns have missing values:")
            st.write(missing_columns)
            missing_value_methods = {}
            for column in missing_columns:
                if df[column].dtype in ['int64', 'float64']:
                    method = st.selectbox(f"Select imputation method for '{column}'", ['Mean', 'Median'], key=f"method_{column}")
                else:
                    method = 'Mode'
                df = handle_missing_values(df, column, method)
                missing_value_methods[column] = method
            st.session_state.missing_value_methods = missing_value_methods
            st.write("Dataset after handling missing values:")
            st.write(df)
        else:
            st.write("No missing values found in the dataset.")
        st.session_state.df = df

if st.session_state.step == 4:
    st.write("### Step 4: Standardization or Normalization")
    if st.session_state.df is not None:
        df = st.session_state.df
        scaling_method = st.selectbox("Select scaling method", ['None', 'Standardization', 'Normalization'], key="scaling_method")
        if scaling_method != st.session_state.scaling_method:
            st.session_state.scaling_method = scaling_method
        if scaling_method == 'Standardization':
            scaler = StandardScaler()
            df_scaled = scaler.fit_transform(df.select_dtypes(include=['int64', 'float64']))
            df_scaled = pd.DataFrame(df_scaled, columns=df.select_dtypes(include=['int64', 'float64']).columns)
            st.write("Dataset after Standardization:")
            st.write(df_scaled)
        elif scaling_method == 'Normalization':
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df.select_dtypes(include=['int64', 'float64']))
            df_scaled = pd.DataFrame(df_scaled, columns=df.select_dtypes(include=['int64', 'float64']).columns)
            st.write("Dataset after Normalization:")
            st.write(df_scaled)
        else:
            df_scaled = df.copy()  # No scaling applied
            st.write("No scaling applied.")
        st.session_state.df_scaled = df_scaled

if st.session_state.step == 5:
    st.write("### Step 5: Remove Outliers using IQR")
    if st.session_state.df_scaled is not None:
        df_scaled = st.session_state.df_scaled
        numeric_columns = df_scaled.select_dtypes(include=['int64', 'float64']).columns
        selected_outlier_columns = st.multiselect("Select columns for outlier removal", numeric_columns, default=st.session_state.outlier_columns)
        st.session_state.outlier_columns = selected_outlier_columns
        for column in selected_outlier_columns:
            df_scaled = remove_outliers(df_scaled, column)
            st.write(f"Dataset after removing outliers in '{column}':")
            st.write(df_scaled)
        st.session_state.df_scaled = df_scaled

if st.session_state.step == 6:
    st.write("### Step 6: Feature Selection")
    if st.session_state.df_scaled is not None:
        df_scaled = st.session_state.df_scaled
        target_variable = st.session_state.target_variable
        feature_columns = [col for col in df_scaled.columns if col != target_variable]
        selected_features = st.multiselect("Select features for model training", feature_columns, default=st.session_state.selected_features)
        st.session_state.selected_features = selected_features
        st.write("Selected features:", selected_features)

if st.session_state.step == 7:
    st.write("### Step 7: Model Selection")
    if st.session_state.df_scaled is not None and st.session_state.selected_features:
        df_scaled = st.session_state.df_scaled
        target_variable = st.session_state.target_variable
        selected_features = st.session_state.selected_features
        model_type = st.selectbox("Select the model", ['Linear Regression', 'Logistic Regression'],
                                  index=['Linear Regression', 'Logistic Regression'].index(st.session_state.model_type), key="model_type")
        # Validate target variable based on model type
        y = df_scaled[target_variable]
        if model_type == 'Logistic Regression':
            if y.dtype in ['int64', 'float64'] and len(y.unique()) > 2:
                st.error("The target variable is continuous. Logistic Regression requires a categorical target variable.")
            elif y.dtype not in ['int64', 'float64']:
                encoder = LabelEncoder()
                y = encoder.fit_transform(y)
                st.session_state.y_encoded = True
            else:
                st.session_state.y_encoded = False
        else:
            st.session_state.y_encoded = False

        if st.button("Train Model"):
            if not selected_features:
                st.error("Please select at least one feature for training.")
            else:
                X = df_scaled[selected_features]
                y = df_scaled[target_variable]
                if st.session_state.y_encoded:
                    encoder = LabelEncoder()
                    y = encoder.fit_transform(y)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                if model_type == 'Linear Regression':
                    model = LinearRegression()
                else:
                    model = LogisticRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                if model_type == 'Linear Regression':
                    mse = mean_squared_error(y_test, y_pred)
                    st.write(f"Mean Squared Error: {mse}")
                else:
                    accuracy = accuracy_score(y_test, y_pred)
                    st.write(f"Model Accuracy: {accuracy}")

if st.session_state.step == 8:
    # Generate missing value handling code
    missing_value_code = ""
    for column, method in st.session_state.get("missing_value_methods", {}).items():
        if method == "Mean":
            missing_value_code += f"df['{column}'].fillna(df['{column}'].mean(), inplace=True)\n"
        elif method == "Median":
            missing_value_code += f"df['{column}'].fillna(df['{column}'].median(), inplace=True)\n"
        elif method == "Mode":
            missing_value_code += f"df['{column}'].fillna(df['{column}'].mode()[0], inplace=True)\n"

    # Generate scaling code
    scaling_code = ""
    if st.session_state.scaling_method == "Standardization":
        scaling_code = """
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df.select_dtypes(include=['int64', 'float64']))
df_scaled = pd.DataFrame(df_scaled, columns=df.select_dtypes(include=['int64', 'float64']).columns)
"""
    elif st.session_state.scaling_method == "Normalization":
        scaling_code = """
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df.select_dtypes(include=['int64', 'float64']))
df_scaled = pd.DataFrame(df_scaled, columns=df.select_dtypes(include=['int64', 'float64']).columns)
"""
    else:
        scaling_code = "df_scaled = df.copy()  # No scaling applied\n"

    # Generate outlier removal code
    outlier_code = ""
    for column in st.session_state.outlier_columns:
        outlier_code += f"""
Q1 = df_scaled['{column}'].quantile(0.25)
Q3 = df_scaled['{column}'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df_scaled = df_scaled[(df_scaled['{column}'] >= lower_bound) & (df_scaled['{column}'] <= upper_bound)]
"""

    # Generate feature selection code
    selected_features_code = ", ".join([f'"{feature}"' for feature in st.session_state.selected_features])

    # Generate target encoding code
    target_encoding_code = ""
    if st.session_state.y_encoded:
        target_encoding_code = """
encoder = LabelEncoder()
y = encoder.fit_transform(y)
"""

    # Generate model selection code
    model_type_code = (
        "LinearRegression()" if st.session_state.model_type == "Linear Regression" else "LogisticRegression()"
    )

    # Assemble the full Python code
    code = f"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv('your_dataset.csv')

# Handle missing values
{missing_value_code}

# Apply scaling
{scaling_code}

# Remove outliers
{outlier_code}

# Feature selection
X = df_scaled[[{selected_features_code}]]  # Selected features
y = df_scaled['{st.session_state.target_variable}']

# Encode target variable for Logistic Regression
{target_encoding_code}

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model selection and training
model = {model_type_code}
model.fit(X_train, y_train)

# Evaluate the model
if isinstance(model, LinearRegression):
    y_pred = model.predict(X_test)
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
elif isinstance(model, LogisticRegression):
    y_pred = model.predict(X_test)
    print("Accuracy Score:", accuracy_score(y_test, y_pred))
"""

    st.code(code, language="python")  # Display the generated code