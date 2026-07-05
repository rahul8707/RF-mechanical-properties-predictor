import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load("random_forest_model.pkl")

st.title("Soft Tissue Mechanical Property Prediction")
st.write("Predict mechanical property value in MPa using a Random Forest model.")

# -----------------------------
# Input fields
# -----------------------------
st.sidebar.header("Enter input features")

# Example input fields
architecture = st.sidebar.selectbox(
    "Architecture",
    ["Grid", "Mesh", "Honeycomb", "Lattice", "Gyroid", "Bulk", "Unknown"]
)

GelMA = st.sidebar.number_input("GelMA (%)", min_value=0.0, max_value=100.0, value=0.0)
Alginate = st.sidebar.number_input("Alginate (%)", min_value=0.0, max_value=100.0, value=0.0)
Collagen = st.sidebar.number_input("Collagen (%)", min_value=0.0, max_value=100.0, value=0.0)
PEG = st.sidebar.number_input("PEG (%)", min_value=0.0, max_value=100.0, value=0.0)
HA = st.sidebar.number_input("HA (%)", min_value=0.0, max_value=100.0, value=0.0)

# Add other features if your model used them
pore_size_um = st.sidebar.number_input("Pore size (µm)", value=0.0)
fiber_diameter_um = st.sidebar.number_input("Fiber diameter (µm)", value=0.0)
printing_pressure_kpa = st.sidebar.number_input("Printing pressure (kPa)", value=0.0)
printing_speed_mm_s = st.sidebar.number_input("Printing speed (mm/s)", value=0.0)

# -----------------------------
# Create input dataframe
# -----------------------------
input_data = pd.DataFrame({
    "architecture": [architecture],
    "GelMA": [GelMA],
    "Alginate": [Alginate],
    "Collagen": [Collagen],
    "PEG": [PEG],
    "HA": [HA],
    "pore_size_um": [pore_size_um],
    "fiber_diameter_um": [fiber_diameter_um],
    "printing_pressure_kpa": [printing_pressure_kpa],
    "printing_speed_mm_s": [printing_speed_mm_s],
})

st.subheader("Input Data")
st.dataframe(input_data)

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict"):
    prediction = model.predict(input_data)

    st.success(f"Predicted value: {prediction[0]:.4f} MPa")