import streamlit as st
import json
from cv_risk_calculators import run_all_risk_assessments

st.set_page_config(page_title="CV Risk Assistant", layout="wide")

st.title("🫀 Cardiovascular Risk Assistant")

# ------------------------
# Helper NA input function
# ------------------------
def optional_number(label):
    col1, col2 = st.columns([3,1])
    val = col1.number_input(label, value=0.0)
    na = col2.checkbox("NA", key=label)
    return None if na else val

# ------------------------
# Patient Inputs
# ------------------------
st.header("Patient Data")

age = optional_number("Age")
sex = st.selectbox("Sex", ["Male","Female"])

ldl = optional_number("LDL")
hdl = optional_number("HDL")
tc = optional_number("Total Cholesterol")
tg = optional_number("Triglycerides")
hba1c = optional_number("HbA1c")
sbp = optional_number("Systolic BP")

st.subheader("Therapy Status")
statin = st.selectbox(
    "Current Statin Therapy",
    ["No statin","Moderate intensity","High intensity"]
)

diabetes_tx = st.selectbox(
    "Diabetes Treatment",
    ["No diabetes","Untreated","Oral therapy","Insulin"]
)

# ------------------------
# PDF Upload
# ------------------------
st.header("Upload Lab Report (optional)")
pdf = st.file_uploader("Upload PDF", type=["pdf"])

if pdf:
    st.info("PDF received. Extraction will work after AI key is added.")

# ------------------------
# Calculate
# ------------------------
if st.button("Calculate Risk"):
    
    patient = {
        "age":age,"sex":sex,
        "ldl":ldl,"hdl":hdl,"tc":tc,"tg":tg,
        "hba1c":hba1c,"sbp":sbp,
        "statin":statin,
        "diabetes_tx":diabetes_tx
    }

    results = run_all_risk_assessments(patient)

    st.header("Risk Results")

    for name,data in results.items():
        if data["status"]=="not_calculable":
            st.warning(f"{name}: Not calculable ({data['reason']})")
        else:
            st.success(f"{name}: {data['value']}")

    # ---------------- AI Interpretation (placeholder)
    # ----------------
    st.header("Clinical Interpretation")

    st.code(json.dumps({"patient":patient,"results":results},indent=2))

    st.info("AI interpretation will activate after API key is added.")