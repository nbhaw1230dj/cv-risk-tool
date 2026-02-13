import streamlit as st
import os
from pypdf import PdfReader
from openai import OpenAI

# ================= UI THEME =================
st.set_page_config(page_title="Cardiovascular Risk Assessment", page_icon="❤️", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1100px; padding-top: 2rem;}
.section-card {
    background: #ffffff;
    padding: 22px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.section-title {font-size:20px;font-weight:600;margin-bottom:12px;}
.main-title {font-size:34px;font-weight:700;}
.sub-title {color:#6b7280;margin-bottom:15px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">❤️ Cardiovascular Risk Assessment</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Evidence-based clinical decision assistant</div>', unsafe_allow_html=True)
st.markdown("---")

# ================= PDF UPLOAD =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📄 Upload Blood Report</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload lab report PDF", type=["pdf"])
pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        pdf_text += page.extract_text()

    st.success("PDF loaded — AI will auto-extract values")

st.markdown('</div>', unsafe_allow_html=True)

# ================= DEMOGRAPHICS =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Demographics</div>', unsafe_allow_html=True)

col1,col2,col3 = st.columns(3)
age = col1.number_input("Age",0,120,40)
sex = col2.selectbox("Sex",["Male","Female"])
race = col3.selectbox("Race/Ethnicity",["Asian","White","Black","Other"])

st.markdown('</div>', unsafe_allow_html=True)

# ================= VITALS =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🩺 Vital Signs</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
sbp = c1.number_input("Systolic BP",0,300,120)
dbp = c2.number_input("Diastolic BP",0,200,80)
height = c3.number_input("Height cm",100,220,170)
weight = c4.number_input("Weight kg",30,200,70)

st.markdown('</div>', unsafe_allow_html=True)

# ================= LABS =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧪 Laboratory Values</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
ldl = c1.number_input("LDL",0.0,500.0,100.0)
hdl = c2.number_input("HDL",0.0,150.0,45.0)
tc = c3.number_input("Total Cholesterol",0.0,600.0,200.0)
tg = c4.number_input("Triglycerides",0.0,600.0,150.0)

hba1c = st.number_input("HbA1c",3.0,15.0,5.5)

st.markdown('</div>', unsafe_allow_html=True)

# ================= HISTORY =================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧠 Medical History</div>', unsafe_allow_html=True)

diabetes = st.checkbox("Diabetes")
hypertension = st.checkbox("Hypertension")
statin = st.checkbox("Currently on statin therapy")
t2dm_meds = st.checkbox("On diabetes medications")
smoker = st.checkbox("Current smoker")

st.markdown('</div>', unsafe_allow_html=True)

# ================= RISK CALC (simple placeholder) =================
def simple_risk():
    score = 0
    if age>55: score+=2
    if ldl>160: score+=2
    if hba1c>=6.5: score+=2
    if smoker: score+=2
    if hypertension: score+=1
    return min(score*5,40)

# ================= RESULTS =================
if st.button("Calculate Risk"):

    risk = simple_risk()

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Risk Results</div>', unsafe_allow_html=True)
    st.write(f"Estimated 10-year CVD risk: **{risk}%**")
    st.markdown('</div>', unsafe_allow_html=True)

    # ================= AI SUMMARY =================
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        prompt = f"""
You are a cardiologist.

Patient:
Age {age}, {sex}
LDL {ldl}, HDL {hdl}, HbA1c {hba1c}
BP {sbp}/{dbp}
Diabetes {diabetes}
Statin {statin}

Give:
1) Statin recommendation
2) Additional drug therapy
3) Indian veg + nonveg diet advice
4) Weight loss calorie deficit
5) Cardio minutes/week
6) Strength training plan
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🩺 Cardiologist Recommendations</div>', unsafe_allow_html=True)
        st.write(response.choices[0].message.content)
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.warning("AI summary unavailable — check API key")
