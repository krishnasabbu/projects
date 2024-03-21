import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Excel Visualize!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Sample Excel Store")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# Function to process uploaded files and merge them into a single DataFrame
def merge_uploaded_files(uploaded_files):
    dfs = []
    for uploaded_file in uploaded_files:
        df = pd.read_excel(uploaded_file)
        dfs.append(df)
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df


# Upload Excel files
uploaded_files = st.file_uploader("Upload Excel files", accept_multiple_files=True)

if uploaded_files:
    # Merge uploaded files
    merged_df = merge_uploaded_files(uploaded_files)

    # Filter options
    st.sidebar.header("Filter Options")
    column_to_filter = st.sidebar.selectbox("Select column to filter", merged_df.columns)
    filter_value = st.sidebar.text_input(f"Enter value to filter in '{column_to_filter}'", "")

    # Apply filter
    filtered_df = merged_df[merged_df[column_to_filter].astype(str).str.contains(filter_value)]

    # Customization options
    st.sidebar.header("Customization Options")
    num_rows_to_display = st.sidebar.slider("Number of rows to display", min_value=1, max_value=len(filtered_df),
                                            value=min(len(filtered_df), 10))

    # Column selection for hiding
    st.sidebar.header("Column Visibility")
    columns_to_hide = []
    for column in merged_df.columns:
        if st.sidebar.checkbox(column, value=False):
            columns_to_hide.append(column)

    # Hide selected columns from filtered DataFrame
    filtered_df = filtered_df.drop(columns=columns_to_hide, errors='ignore')

    # Display Excel Sheet and Filtered DataFrame
    col1, col2 = st.columns(2)
    with col1:
        # Display merged Excel Sheet
        st.write("Merged Excel Data:", merged_df)
    with col2:
        # Display filtered and customized DataFrame
        st.write("Filtered and Customized Excel Sheet:")
        filtered_table = filtered_df.head(num_rows_to_display)
        st.write(filtered_table)

    col1, col2 = st.columns(2)
    with col1:
        # Create Bar Chart
        st.header("Bar Chart")
        selected_bar_column = st.selectbox("Select a column for bar chart", merged_df.columns)
        bar_data = filtered_df[selected_bar_column].value_counts()
        fig_bar = px.bar(x=bar_data.index, y=bar_data.values, title=f"Bar Chart for {selected_bar_column}")
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        # Create Pie Chart
        st.header("Pie Chart")
        selected_pie_column = st.selectbox("Select a column for pie chart", merged_df.columns)
        pie_data = filtered_df[selected_pie_column].value_counts()
        fig_pie = px.pie(names=pie_data.index, values=pie_data.values, title=f"Pie Chart for {selected_pie_column}")
        st.plotly_chart(fig_pie, use_container_width=True)
