import streamlit as st
from cv_risk_calculators import run_all_risk_assessments

st.set_page_config(layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {padding-top: 2rem;}
.card {
    background-color: #f7f9fc;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 18px;
    border: 1px solid #e6eaf1;
}
.section-title {
    font-size:20px;
    font-weight:600;
    margin-bottom:10px;
}
.bmi-bar {
    background-color:#e9f2ff;
    padding:8px;
    border-radius:8px;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.title("🫀 Cardiovascular Risk Assessment")

# ---------- Demographics ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Demographics</div>', unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)
age = c1.number_input("Age",0,120,40)
sex = c2.selectbox("Sex",["Male","Female"])
eth = c3.selectbox("Race/Ethnicity",["Asian","White","Black","Other"])

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Vitals ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Vital Signs</div>', unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
sbp = c1.number_input("Systolic BP",80,250,120)
dbp = c2.number_input("Diastolic BP",40,150,80)
height = c3.number_input("Height cm",100,220,170)
weight = c4.number_input("Weight kg",30,200,70)
waist = c5.number_input("Waist cm",40,150,80)

bmi = weight/((height/100)**2)
st.markdown(f'<div class="bmi-bar">Calculated BMI: {bmi:.1f} kg/m²</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Labs ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Laboratory Values</div>', unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
tc = c1.number_input("Total Cholesterol",50,400,180)
hdl = c2.number_input("HDL",10,100,45)
ldl = c3.number_input("LDL",10,300,100)
tg = c4.number_input("Triglycerides",30,500,150)
glucose = c5.number_input("Fasting Glucose",50,300,95)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Therapy ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Current Therapy</div>', unsafe_allow_html=True)

c1,c2 = st.columns(2)
statin = c1.selectbox("Statin therapy",["No statin","Moderate intensity","High intensity"])
diabetes_tx = c2.selectbox("Diabetes treatment",["No diabetes","Oral","Insulin"])

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Calculate ----------
if st.button("Calculate Cardiovascular Risk"):

    patient = {
        "age":age,"sex":sex,
        "ldl":ldl,"hdl":hdl,"tc":tc,"tg":tg,
        "sbp":sbp,
        "statin":statin,
        "diabetes_tx":diabetes_tx
    }

    results = run_all_risk_assessments(patient)

    st.header("Results")
    for k,v in results.items():
        if v["status"]=="ok":
            st.success(f"{k}: {v['value']}")
        else:
            st.warning(f"{k}: Not calculable ({v['reason']})")
