import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Mechanical Property Prediction for soft tissue engineering")

st.title("Mechanical Property Prediction for soft tissue engineering")
st.write("Predict mechanical property value in MPa using a Random Forest model.")

# -----------------------------
# Load model
# -----------------------------
MODEL_PATH = Path(__file__).parent / "random_forest_pipeline.pkl"

if not MODEL_PATH.exists():
    st.error("Model file not found. Please upload random_forest_model.pkl to the same folder as app_RF.py.")
    st.stop()

model = joblib.load(MODEL_PATH)

# -----------------------------
# Feature names
# -----------------------------
material_cols = [
    'PEGDA', 'Gellan Gum', 'Gelatin', 'GelMA', 'PCL', 'Alginate',
    'Chitosan', 'HAMA', 'HA', 'Collagen', 'Hydroxyapatite', 'Agarose',
    'PEG', 'Matrigel', 'bioink', 'dECM', 'fibrin', 'Fibrinogen',
    'PLGA', 'PLCL', 'Beta Tricalcium Phosphate', 'PVA',
    'Kappa Carrageenan', 'Nanosilicates', 'Xanthan Gum', 'GAG',
    'Laponite', 'Methylcellulose', 'Transglutaminase',
    'PEG-NIPAAm-HPMACys', 'HA Phenolic Hydroxyl Functionalized',
    'Icariin', 'Silk Fibroin', 'Cellulose'
]

feature_names = [
    'architecture',
    'pore_mean_um'
] + material_cols

# -----------------------------
# Input fields
# -----------------------------
inputs = {}

st.subheader("Scaffold Architecture")

inputs["architecture"] = st.selectbox(
    "Architecture",
    ["Grid", "Mesh", "Honeycomb", "Gyroid", "Bulk", "Lattice", "Unknown"]
)

inputs["pore_mean_um"] = st.number_input(
    "Pore mean size (µm)",
    min_value=0.0,
    value=0.0,
    step=1.0
)

# Initialize all material columns with 0
for material in material_cols:
    inputs[material] = 0.0

st.subheader("Material Composition")

st.write("Select up to 5 materials and enter their percentages.")

for i in range(1, 6):
    col1, col2 = st.columns([2, 1])

    with col1:
        selected_material = st.selectbox(
            f"Material {i}",
            ["None"] + material_cols,
            key=f"material_{i}"
        )

    with col2:
        percentage = st.number_input(
            f"Percentage {i} (%)",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.1,
            key=f"percentage_{i}"
        )

    if selected_material != "None":
        inputs[selected_material] += percentage

# -----------------------------
# Create input dataframe
# -----------------------------
X = pd.DataFrame([inputs])
X = X[feature_names]

# -----------------------------
# Validation
# -----------------------------
total_percentage = X[material_cols].sum(axis=1).iloc[0]

st.write(f"Total material percentage: {total_percentage:.1f}%")

if total_percentage == 0:
    st.warning("Please enter at least one material percentage.")

if total_percentage > 100:
    st.warning("Total material percentage is greater than 100%.")

# -----------------------------
# Show model input
# -----------------------------
with st.expander("Show model input data"):
    st.dataframe(X)

# -----------------------------
# Prediction
# -----------------------------
if st.button("Predict"):

    if total_percentage == 0:
        st.error("Prediction cannot be made because no material composition was entered.")

    elif total_percentage > 100:
        st.error("Prediction cannot be made because total material percentage is greater than 100%.")

    else:
        prediction = model.predict(X)
        st.success(f"Predicted value = {prediction[0]:.3f} MPa")
