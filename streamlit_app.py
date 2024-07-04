import streamlit as st
import pandas as pd
from pandas.api import types

# Show title and description.
st.title("No Code Datascience Project")

# File uploader widget
uploaded_file = st.file_uploader("Upload the dataset (.csv or .xlsx)", type=("csv", "xlsx"))

if uploaded_file is not None:
    # Check the file type
    st.write(uploaded_file.type)
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)

    # Display the first few rows of the dataframe
    st.write("First few rows of the uploaded dataset:")
    st.write(df.head())

    # Allow user to select the target column
    target_column = st.selectbox("Select the target column", df.columns)

    # Optional: Display some information about the selected column
    if target_column:
        st.write(f"Selected target column: {target_column}")
        st.write(f"Data type: {df[target_column].dtype}")
        st.write(f"Number of unique values: {df[target_column].nunique()}")
        
        if types.is_numeric_dtype(df[target_column]):
            st.write('Numerical')
        else:
            st.write('Categorical')

