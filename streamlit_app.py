import streamlit as st
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.exceptions import NotFittedError

# Load the pre-trained model
model = joblib.load("SVM.joblib")  # Use the correct model file

# Define the preprocessor for input features
numerical_cols = ['age', 'trestbps', 'chol', 'thalach']  # Update as per your data
categorical_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']  # Update as per your data

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Fit the preprocessor on the entire dataset (assuming you have access to it)
# For the purpose of this example, let's create a dummy dataframe to fit the preprocessor
dummy_data = pd.DataFrame({
    'age': [50],
    'sex': [1],
    'cp': [0],
    'trestbps': [120],
    'chol': [200],
    'fbs': [0],
    'restecg': [1],
    'thalach': [150],
    'exang': [0],
    'slope': [1],
    'ca': [0],
    'thal': [2]
})
preprocessor.fit(dummy_data)

# Streamlit app
st.title("Heart Disease Prediction")

# Collect user input
st.header("Enter patient details:")
age = st.number_input("Age", min_value=10, max_value=120, value=50)
sex = st.selectbox("Sex", options=[0, 1], format_func=lambda x: "Female" if x == 0 else "Male")
cp = st.selectbox("Chest Pain Type (cp)", options=[0, 1, 2, 3])
trestbps = st.number_input("Resting Blood Pressure (trestbps)", min_value=70, max_value=300, value=120)
chol = st.number_input("Serum Cholesterol (chol)", min_value=100, max_value=600, value=200)
fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", options=[0, 1])
restecg = st.selectbox("Resting Electrocardiographic Results (restecg)", options=[0, 1, 2])
thalach = st.number_input("Maximum Heart Rate Achieved (thalach)", min_value=50, max_value=250, value=150)
exang = st.selectbox("Exercise Induced Angina (exang)", options=[0, 1])
slope = st.selectbox("Slope of the Peak Exercise ST Segment (slope)", options=[0, 1, 2])
ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy (ca)", options=[0, 1, 2, 3, 4])
thal = st.selectbox("Thalassemia (thal)", options=[0, 1, 2, 3])

# Create a DataFrame for the input
input_data = pd.DataFrame({
    'age': [age],
    'sex': [sex],
    'cp': [cp],
    'trestbps': [trestbps],
    'chol': [chol],
    'fbs': [fbs],
    'restecg': [restecg],
    'thalach': [thalach],
    'exang': [exang],
    'slope': [slope],
    'ca': [ca],
    'thal': [thal]
})

# Preprocess the input data
try:
    input_data_preprocessed = preprocessor.transform(input_data)
except NotFittedError as e:
    st.error(f"Error: {e}")

# Predict and display the result
if st.button("Predict"):
    try:
        prediction = model.predict(input_data_preprocessed)
        if prediction[0] == 1:
            st.write("The patient is likely to have heart disease.")
        else:
            st.write("The patient is not likely to have heart disease.")
    except ValueError as e:
        st.error(f"Prediction error: {e}")

# Add additional sections as needed
st.header("Application Information")
st.write("This application helps medical practitioners predict the likelihood of heart disease based on patient details.")
