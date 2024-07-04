import streamlit as st
import pandas as pd
import time
from pandas.api import types
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Function to determine if a column is discrete
def is_discrete(column):
    unique_values_ratio = len(column.unique()) / len(column)
    if unique_values_ratio < 0.1:
        return True
    return False

# Function to determine if a column is numerical or categorical
def is_numerical(column):
    return types.is_numeric_dtype(column)

def select_features(df, target_column):
    if is_numerical(df[target_column]):
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[float, int])
        # For numerical target, use correlation
        corr_matrix = numeric_df.corr()
        correlations = corr_matrix[target_column].abs().sort_values(ascending=False)
        selected_features = correlations.index[1:]  # Exclude target column itself
        return selected_features

# Show title and description
st.title("No Code Datascience Project")

# File uploader widget
uploaded_file = st.file_uploader("Upload the dataset (.csv or .xlsx)", type=("csv", "xlsx"))

if uploaded_file is not None:
    # Check the file type
    if uploaded_file.type == "text/csv":
        uploaded_dataset = pd.read_csv(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        uploaded_dataset = pd.read_excel(uploaded_file, engine='openpyxl')
    else:
        st.error("Please upload a valid document from the above-mentioned types")

    # Display the first few rows of the dataframe
    st.write("First few rows of the uploaded dataset:")
    st.write(uploaded_dataset.head())
    
    # Drop columns that contain any of the specified keywords
    keywords_to_exclude = ['id', 'name', 'contact']
    columns_to_exclude = [col for col in uploaded_dataset.columns if any(keyword in col.lower() for keyword in keywords_to_exclude)]
    if columns_to_exclude:
        uploaded_dataset = uploaded_dataset.drop(columns=columns_to_exclude)
        
    target_column = st.selectbox("Select the target column", uploaded_dataset.columns)

    if target_column:
        st.write(f"Selected target column: {target_column}")
        st.write(f"Data type: {uploaded_dataset[target_column].dtype}")
        st.write(f"Number of unique values: {uploaded_dataset[target_column].nunique()}")

        if is_numerical(uploaded_dataset[target_column]):
            selected_features = select_features(uploaded_dataset, target_column)
            st.write("The selected column is numerical.")
            st.write(f"Selected features: {list(selected_features)}")
            
            if is_discrete(uploaded_dataset[target_column]):
                st.write("The target column is discrete.")
            else:
                X = uploaded_dataset[selected_features]
                y = uploaded_dataset[target_column]
                X_train, X_test, y_train, y_test = train_test_split(X, y)
                
                lr = LinearRegression()
                lr.fit(X_train, y_train)
                st.success("Model Trained Successfully")

                # User input for prediction
                st.write("Enter the feature values for prediction:")
                input_values = {}
                for feature in selected_features:
                    input_values[feature] = st.number_input(f'Enter {feature}')

                input_pred = pd.DataFrame([input_values])
                st.write("Input for prediction:")
                st.write(input_pred)

                # Make prediction based on user input
                if st.button('Predict'):
                    user_pred = lr.predict(input_pred)
                    st.write(f"Your Prediction is {user_pred[0]}")
                
        else:
            st.write("The selected column is categorical.")
