import streamlit as st
from cv_risk_calculators import run_all_risk_assessments
from pypdf import PdfReader
import re
from openai import OpenAI
import os

st.set_page_config(layout="wide")
st.title("🫀 Cardiovascular Risk Assessment")

# ------------------- OPENAI -------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------- HELPERS -------------------
def extract_value(pattern,text):
    m = re.search(pattern,text,re.IGNORECASE)
    return float(m.group(1)) if m else None

def safe_input(label,default):
    col1,col2 = st.columns([4,1])
    val = col1.number_input(label,value=default)
    na = col2.checkbox("NA",key=label)
    return None if na else val

def generate_report(patient,results):

    prompt=f"""
You are a preventive cardiologist.

Analyze this patient and produce a structured clinical report.

PATIENT DATA:
{patient}

RISK SCORES:
{results}

Write sections:

1. Global cardiovascular risk interpretation
2. Lipid lowering therapy recommendation (drug + intensity + LDL goal)
3. Need for ezetimibe / PCSK9 / fibrate
4. Diabetes cardioprotective drugs
5. Aspirin indication
6. Indian diet plan (veg and non veg options separately)
7. Calorie deficit and weight target
8. Strength + cardio exercise prescription (days/week + minutes)
"""

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    return res.choices[0].message.content

# ------------------- PDF UPLOAD -------------------
st.header("Upload Blood Report")
uploaded = st.file_uploader("Upload lab report PDF",type="pdf")

pdf_vals={}
if uploaded:
    reader = PdfReader(uploaded)
    text=""
    for p in reader.pages:
        if p.extract_text():
            text+=p.extract_text()

    pdf_vals["ldl"]=extract_value(r"LDL[^0-9]*([\d.]+)",text)
    pdf_vals["hdl"]=extract_value(r"HDL[^0-9]*([\d.]+)",text)
    pdf_vals["tc"]=extract_value(r"Total Cholesterol[^0-9]*([\d.]+)",text)
    pdf_vals["tg"]=extract_value(r"Triglycerides[^0-9]*([\d.]+)",text)
    pdf_vals["hba1c"]=extract_value(r"HbA1c[^0-9]*([\d.]+)",text)

    st.success("Lab values extracted from PDF")

# ------------------- DEMOGRAPHICS -------------------
st.header("Demographics")
c1,c2,c3=st.columns(3)
age=safe_input("Age",40)
sex=c2.selectbox("Sex",["Male","Female"])
race=c3.selectbox("Race/Ethnicity",["Asian","White","Black","Other"])

# ------------------- VITALS -------------------
st.header("Vital Signs")
sbp=safe_input("Systolic BP",120)
dbp=safe_input("Diastolic BP",80)
height=safe_input("Height cm",170)
weight=safe_input("Weight kg",70)
waist=safe_input("Waist cm",80)

bmi=None
if height and weight:
    bmi=weight/((height/100)**2)
    st.info(f"BMI: {bmi:.1f}")

# ------------------- LABS -------------------
st.header("Laboratory Values")
tc=safe_input("Total Cholesterol",pdf_vals.get("tc",180))
hdl=safe_input("HDL",pdf_vals.get("hdl",45))
ldl=safe_input("LDL",pdf_vals.get("ldl",100))
tg=safe_input("Triglycerides",pdf_vals.get("tg",150))
hba1c=safe_input("HbA1c",pdf_vals.get("hba1c",5.6))

# ------------------- HISTORY -------------------
st.header("Medical History")
diabetes=st.selectbox("Diabetes status",["None","Prediabetes","Diabetes"])
htn_tx=st.checkbox("On hypertension treatment")
ckd=st.checkbox("CKD stage 3+")
hf=st.checkbox("Heart failure")
af=st.checkbox("Atrial fibrillation")
prior_mi=st.checkbox("Prior MI")
prior_stroke=st.checkbox("Prior stroke/TIA")
revasc=st.checkbox("PCI/CABG")
pad=st.checkbox("Peripheral artery disease")

# ------------------- FAMILY -------------------
st.header("Family History")
premature_cvd=st.checkbox("Premature CVD in first-degree relative")
fh_diabetes=st.checkbox("Family history diabetes")

# ------------------- LIFESTYLE -------------------
st.header("Lifestyle")
smoking=st.selectbox("Smoking status",["Never","Former","Current"])

# ------------------- THERAPY -------------------
st.header("Current Therapy")
statin=st.selectbox("Statin therapy",["No statin","Moderate intensity","High intensity"])
dm_tx=st.selectbox("Diabetes treatment",["None","Oral","Insulin"])

# ------------------- CALCULATE -------------------
if st.button("Calculate Risk"):

    patient={
        "age":age,"sex":sex,"race":race,"sbp":sbp,"dbp":dbp,"bmi":bmi,
        "ldl":ldl,"hdl":hdl,"tc":tc,"tg":tg,"hba1c":hba1c,
        "diabetes":diabetes,"smoking":smoking,
        "htn_tx":htn_tx,"ckd":ckd,"hf":hf,"af":af,
        "prior_mi":prior_mi,"prior_stroke":prior_stroke,"revasc":revasc,"pad":pad,
        "premature_cvd":premature_cvd,"fh_diabetes":fh_diabetes,
        "statin":statin,"dm_tx":dm_tx
    }

    results=run_all_risk_assessments(patient)

    st.header("Risk Scores")
    for k,v in results.items():
        if v["status"]=="ok":
            st.success(f"{k}: {v['value']}")
        else:
            st.warning(f"{k}: Not calculable ({v['reason']})")

    st.header("Clinical Cardiologist Summary")
    report=generate_report(patient,results)
    st.markdown(report)
