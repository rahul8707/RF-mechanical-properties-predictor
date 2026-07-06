import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("random_forest_model.pkl")

st.set_page_config(page_title="Mechanical Property Prediction")

st.title("Mechanical Property Prediction")
st.write("Predict Young's modulus / mechanical property (MPa).")

# -----------------------------------
# IMPORTANT:
# Replace these with YOUR feature names
# -----------------------------------
feature_names = [
    'architecture','pore_mean_um', 'PEGDA', 'Gellan Gum', 'Gelatin', 'GelMA', 'PCL', 'Alginate', 'Chitosan', 'HAMA', 'HA', 'Collagen', 'Hydroxyapatite', 'Agarose', 'PEG', 'Matrigel', 'bioink', 'dECM', 'fibrin', 'Fibrinogen', 'PLGA', 'PLCL', 'Beta Tricalcium Phosphate', 'PVA', 'Kappa Carrageenan', 'Nanosilicates', 'Xanthan Gum', 'GAG', 'Laponite', 'Methylcellulose', 'Transglutaminase', 'PEG-NIPAAm-HPMACys', 'HA Phenolic Hydroxyl Functionalized', 'Icariin', 'Silk Fibroin', 'Cellulose'
]

inputs = {}

for feature in feature_names:

    if feature == "architecture":
        inputs[feature] = st.selectbox(
            feature,
            ["Grid", "Mesh", "Honeycomb", "Gyroid", "Bulk", "Lattice", "Unknown"]
        )
    else:
        inputs[feature] = st.number_input(
            feature,
            min_value=0.0,
            value=0.0,
            step=0.1
        )

X = pd.DataFrame([inputs])

if st.button("Predict"):

    prediction = model.predict(X)

    st.success(f"Predicted value = {prediction[0]:.3f} MPa")