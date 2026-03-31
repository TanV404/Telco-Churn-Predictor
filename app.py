import streamlit as st
import numpy as np
import pandas as pd
import pickle

# Load artifacts
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
feature_names = pickle.load(open("features.pkl", "rb"))

st.title("📊 Customer Churn Predictor")

st.write("Enter customer details:")

# --- USER INPUTS ---
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
total_charges = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
online_security = st.selectbox("Online Security", ["Yes", "No"])

# --- CREATE INPUT DATAFRAME ---
input_dict = {col: 0 for col in feature_names}

# Fill basic features
input_dict['tenure'] = tenure
input_dict['MonthlyCharges'] = monthly_charges
input_dict['TotalCharges'] = total_charges

# Contract encoding
if contract == "One year":
    input_dict['Contract_One year'] = 1
elif contract == "Two year":
    input_dict['Contract_Two year'] = 1

# Online Security encoding
if online_security == "Yes":
    input_dict['OnlineSecurity_Yes'] = 1

# Convert to DataFrame
input_df = pd.DataFrame([input_dict])

# Scale
input_scaled = scaler.transform(input_df)

# --- PREDICTION ---
if st.button("Predict"):
    prob = model.predict_proba(input_scaled)[0][1]

    if prob > 0.3:
        st.error(f"⚠️ High Risk of Churn ({prob:.2f})")
    else:
        st.success(f"✅ Low Risk of Churn ({prob:.2f})")