import streamlit as st
import pandas as pd

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Read Excel file
    df = pd.read_excel(uploaded_file)

    # Display DataFrame
    st.write("Excel Sheet:", df)

    # Filter options
    st.sidebar.header("Filter Options")
    column_to_filter = st.sidebar.selectbox("Select column to filter", df.columns)
    filter_value = st.sidebar.text_input(f"Enter value to filter in '{column_to_filter}'", "")

    # Apply filter
    filtered_df = df[df[column_to_filter].astype(str).str.contains(filter_value)]

    # Customization options
    st.sidebar.header("Customization Options")
    num_rows_to_display = st.sidebar.slider("Number of rows to display", min_value=1, max_value=len(filtered_df),
                                            value=min(len(filtered_df), 10))
    show_index = st.sidebar.checkbox("Show DataFrame index", value=False)

    # Column selection for hiding
    st.sidebar.header("Column Visibility")
    columns_to_hide = []
    for column in df.columns:
        if st.sidebar.checkbox(column, value=False):
            columns_to_hide.append(column)

    # Hide selected columns from filtered DataFrame
    filtered_df = filtered_df.drop(columns=columns_to_hide, errors='ignore')

    # Display filtered and customized DataFrame in a table
    st.write("Filtered and Customized Excel Sheet:")
    if show_index:
        st.write(filtered_df.head(num_rows_to_display))
    else:
        st.write(filtered_df.head(num_rows_to_display).to_string(index=False))
