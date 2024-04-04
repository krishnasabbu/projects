import streamlit as st
import pandas as pd
import plotly.express as px
import warnings
from streamlit_modal import Modal

modal = Modal(key="Mapping Key", title="Map Primary Keys")

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Excel Visualize!!!", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Sample Excel Store")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Upload Excel files
uploaded_files = st.file_uploader("Upload Excel files", accept_multiple_files=True)

if 'primary_key_df1' not in st.session_state:
    st.session_state.primary_key_df1 = ''

if 'primary_key_df2' not in st.session_state:
    st.session_state.primary_key_df2 = ''

if uploaded_files:

    dfs = [pd.read_excel(file) for file in uploaded_files]

    if len(dfs) == 2:

        col1, col2 = st.columns(2)
        with col1:
            # Display merged Excel Sheet
            st.write("First Excel :", dfs[0])
        with col2:
            st.write("Second Excel:", dfs[1])

        # Concatenate column names of both DataFrames
        columns_df1 = dfs[0].columns.tolist()
        columns_df2 = dfs[1].columns.tolist()

        if len(st.session_state.primary_key_df1) != 0 and len(st.session_state.primary_key_df2) != 0:
            merged_df = pd.merge(dfs[0], dfs[1], how='outer', left_on=st.session_state.primary_key_df1,
                                 right_on=st.session_state.primary_key_df2)
        else:
            merged_df = dfs[0]

        # Modal for configuration
        with st.sidebar:

            configuration = st.button('Mapping Configuration')

            if configuration:
                modal.open()

            if modal.is_open():
                with modal.container():
                    # Modal for configuration
                    with st.form(key='configuration_form'):
                        st.write("Columns of first DataFrame:")
                        st.write(columns_df1)

                        st.write("Columns of second DataFrame:")
                        st.write(columns_df2)

                        st.subheader('Field Mapping Configuration')
                        st.session_state.primary_key_df1 = st.selectbox("Select primary key for first DataFrame",
                                                                        columns_df1)
                        st.session_state.primary_key_df2 = st.selectbox("Select primary key for second DataFrame",
                                                                        columns_df2)

                        submitted = st.form_submit_button('Merge')

                        if submitted:
                            merged_df = pd.merge(dfs[0], dfs[1], how='outer', left_on=st.session_state.primary_key_df1,
                                                 right_on=st.session_state.primary_key_df2)
                            modal.close()
                        else:
                            merged_df = dfs[0]

    else:
        merged_df = dfs[0]
        st.write("First Excel Sheet:")
        st.write(merged_df)

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
