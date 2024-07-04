import streamlit as st
import pandas as pd


# Show title and description.
st.title("No Code Datascience Project")
# File uploader widget
uploaded_file = st.file_uploader("Upload the dataset (.csv or .xlsx)", type=("csv", "xlsx"))

if uploaded_file is not None:
    # Check the file type
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)

    # Display the first few rows of the dataframe
    st.write("First few rows of the uploaded dataset:")
    st.write(df.head())
