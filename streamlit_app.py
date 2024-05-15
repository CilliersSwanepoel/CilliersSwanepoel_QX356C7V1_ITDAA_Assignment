import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('K-Nearest Neighbors.joblib')
preprocessor = joblib.load('preprocessor.joblib')

st.title("Heart Disease Prediction App")
st.write("Enter the details of the patient to predict the likelihood of heart disease.")

with st.form("patient_form"):
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    sex = st.selectbox("Sex", options=["Male", "Female"])
    cp = st.selectbox("Chest Pain Type", options=["Type 1", "Type 2", "Type 3", "Type 4"])
    trestbps = st.number_input("Resting Blood Pressure", min_value=0, step=1)
    chol = st.number_input("Serum Cholesterol", min_value=0, step=1)
    fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["Yes", "No"])
    restecg = st.selectbox("Resting Electrocardiographic Results", options=["Normal", "Having ST-T wave abnormality", "Showing probable or definite left ventricular hypertrophy"])
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=0, step=1)
    exang = st.selectbox("Exercise Induced Angina", options=["Yes", "No"])
    oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, step=0.1)
    slope = st.selectbox("Slope of the Peak Exercise ST Segment", options=["Upsloping", "Flat", "Downsloping"])
    ca = st.number_input("Number of Major Vessels Colored by Fluoroscopy", min_value=0, max_value=4, step=1)
    thal = st.selectbox("Thalassemia", options=["Normal", "Fixed Defect", "Reversible Defect"])

    submit_button = st.form_submit_button(label='Predict')

if submit_button:

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
        'oldpeak': [oldpeak],
        'slope': [slope],
        'ca': [ca],
        'thal': [thal]
    })


    input_data['sex'] = input_data['sex'].map({'Male': 1, 'Female': 0})
    input_data['fbs'] = input_data['fbs'].map({'Yes': 1, 'No': 0})
    input_data['exang'] = input_data['exang'].map({'Yes': 1, 'No': 0})
    input_data['cp'] = input_data['cp'].map({"Type 1": 0, "Type 2": 1, "Type 3": 2, "Type 4": 3})
    input_data['restecg'] = input_data['restecg'].map({"Normal": 0, "Having ST-T wave abnormality": 1, "Showing probable or definite left ventricular hypertrophy": 2})
    input_data['slope'] = input_data['slope'].map({"Upsloping": 0, "Flat": 1, "Downsloping": 2})
    input_data['thal'] = input_data['thal'].map({"Normal": 1, "Fixed Defect": 2, "Reversible Defect": 3})

    try:
       
        input_data_preprocessed = preprocessor.transform(input_data)

      
        prediction = model.predict(input_data_preprocessed)
        result = "Heart Disease Detected" if prediction[0] == 1 else "No Heart Disease Detected"
        st.write(f"Prediction: {result}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

