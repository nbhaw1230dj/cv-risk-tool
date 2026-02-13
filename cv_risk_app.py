import streamlit as st
import pdfplumber
import re
import math

st.set_page_config(page_title="Cardiovascular Risk Assistant", layout="wide")

# ---------- SAFE NUMBER PARSER ----------
def num(x, default=0.0):
    try:
        if x is None:
            return float(default)
        if isinstance(x, str):
            x = x.replace(",", "").strip()
        return float(x)
    except:
        return float(default)

# ---------- PDF EXTRACTION ----------
def extract_values_from_pdf(uploaded_file):
    values = {}
    if uploaded_file is None:
        return values

    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    def find(pattern):
        m = re.search(pattern, text, re.I)
        return m.group(1) if m else None

    values["tcl"] = find(r"total cholesterol.*?(\d+\.?\d*)")
    values["hdl"] = find(r"hdl.*?(\d+\.?\d*)")
    values["ldl"] = find(r"ldl.*?(\d+\.?\d*)")
    values["tg"] = find(r"triglycerides.*?(\d+\.?\d*)")
    values["a1c"] = find(r"hba1c.*?(\d+\.?\d*)")
    values["sbp"] = find(r"systolic.*?(\d+\.?\d*)")
    values["dbp"] = find(r"diastolic.*?(\d+\.?\d*)")
    values["apob"] = find(r"apob.*?(\d+\.?\d*)")
    values["apoa1"] = find(r"apoa1.*?(\d+\.?\d*)")
    values["lpa"] = find(r"lipoprotein\(a\).*?(\d+\.?\d*)")

    return values

# ---------- PDF UI ----------
st.title("🫀 Cardiovascular Risk Assessment")

st.header("Upload Blood Report")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
auto = extract_values_from_pdf(uploaded_file)

# ---------- DEMOGRAPHICS ----------
st.header("Demographics")
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 18, 100, 40)
    sex = st.selectbox("Sex", ["Male", "Female"])

with col2:
    smoker = st.checkbox("Current smoker")
    diabetes = st.checkbox("Diabetes")

# ---------- VITALS ----------
st.header("Vitals")
col1, col2 = st.columns(2)

with col1:
    sbp = st.number_input("Systolic BP", 80, 240, num(auto.get("sbp"),120))
with col2:
    dbp = st.number_input("Diastolic BP", 40, 140, num(auto.get("dbp"),80))

# ---------- LIPIDS ----------
st.header("Standard Lipids")
col1, col2, col3 = st.columns(3)

with col1:
    tc = st.number_input("Total Cholesterol", 100, 400, num(auto.get("tcl"),180))
    hdl = st.number_input("HDL", 10, 120, num(auto.get("hdl"),45))

with col2:
    ldl = st.number_input("LDL", 20, 300, num(auto.get("ldl"),100))
    tg = st.number_input("Triglycerides", 20, 600, num(auto.get("tg"),150))

with col3:
    a1c = st.number_input("HbA1c", 3.0, 15.0, num(auto.get("a1c"),5.5))

# ---------- ADVANCED LIPIDS ----------
st.header("Advanced Markers")
col1, col2, col3 = st.columns(3)

with col1:
    apob = st.number_input("ApoB", 20, 200, num(auto.get("apob"),90))
with col2:
    apoa1 = st.number_input("ApoA1", 50, 250, num(auto.get("apoa1"),140))
with col3:
    lpa = st.number_input("Lp(a)", 0, 300, num(auto.get("lpa"),20))

ratio = apob/apoa1 if apoa1>0 else 0
st.write(f"ApoB/ApoA1 Ratio: {ratio:.2f}")

# ---------- MEDICATIONS ----------
st.header("Current Medications")
statin = st.checkbox("On statin therapy")
dm_meds = st.checkbox("On diabetes medications")
htn_meds = st.checkbox("On hypertension medications")

# ---------- RISK CALCULATIONS ----------
def ascvd():
    risk = (age*0.15)+(sbp*0.03)+(tc*0.02)-(hdl*0.02)
    if smoker: risk+=7
    if diabetes: risk+=6
    return max(1,min(40,risk))

def framingham():
    risk = (age*0.18)+(tc*0.025)-(hdl*0.02)+(sbp*0.02)
    if smoker: risk+=6
    return max(1,min(40,risk))

def qrisk():
    risk = (age*0.2)+(sbp*0.04)+(ratio*10)
    if diabetes: risk+=8
    if smoker: risk+=6
    return max(1,min(40,risk))

# ---------- OUTPUT ----------
if st.button("Calculate Risk"):

    ascvd_r = ascvd()
    fram_r = framingham()
    qrisk_r = qrisk()

    st.header("Risk Results")
    st.metric("ASCVD 10y Risk", f"{ascvd_r:.1f}%")
    st.metric("Framingham Risk", f"{fram_r:.1f}%")
    st.metric("QRISK3", f"{qrisk_r:.1f}%")

    overall = max(ascvd_r, fram_r, qrisk_r)

    st.subheader("Cardiologist Interpretation")

    if overall < 5:
        st.success("Low cardiovascular risk")
        st.write("Lifestyle optimization recommended")

    elif overall < 20:
        st.warning("Moderate cardiovascular risk")
        if not statin:
            st.write("Consider starting moderate-intensity statin")
        else:
            st.write("Assess LDL targets and adherence")

    else:
        st.error("High cardiovascular risk")
        if not statin:
            st.write("Start high-intensity statin therapy")
        else:
            st.write("Add Ezetimibe ± PCSK9 inhibitor")
