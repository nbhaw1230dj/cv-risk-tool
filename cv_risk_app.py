import streamlit as st
import math
import pdfplumber
import re

st.set_page_config(layout="wide", page_title="Cardiovascular Risk Assistant")

# =========================================================
# PDF LAB EXTRACTION
# =========================================================
def extract_labs(file):
    labs = {}
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text().lower() + "\n"

        def grab(pattern):
            m = re.search(pattern, text)
            return float(m.group(1)) if m else None

        labs["tc"] = grab(r"total cholesterol[^0-9]*([0-9]+\.?[0-9]*)")
        labs["hdl"] = grab(r"\bhdl[^0-9]*([0-9]+\.?[0-9]*)")
        labs["ldl"] = grab(r"\bldl[^0-9]*([0-9]+\.?[0-9]*)")
        labs["tg"] = grab(r"triglycerides[^0-9]*([0-9]+\.?[0-9]*)")
        labs["hba1c"] = grab(r"hba1c[^0-9]*([0-9]+\.?[0-9]*)")
        labs["apob"] = grab(r"apob[^0-9]*([0-9]+\.?[0-9]*)")
        labs["apoa1"] = grab(r"apoa1[^0-9]*([0-9]+\.?[0-9]*)")
        labs["lpa"] = grab(r"lp\(a\)[^0-9]*([0-9]+\.?[0-9]*)")

    except:
        pass

    return labs

# =========================================================
# HELPERS
# =========================================================
def bmi(ht, wt):
    if ht and wt:
        return round(wt/((ht/100)**2),1)
    return None

def apo_ratio(apob, apoa1):
    if apob and apoa1:
        return round(apob/apoa1,2)
    return None

# Risk Models (clinical approximations)
def ascvd(age, sex, tc, hdl, sbp, smoker, diabetes):
    risk = (age-40)*0.08 + (tc-150)*0.015 - (hdl-50)*0.02 + (sbp-120)*0.02
    if smoker: risk+=4
    if diabetes: risk+=5
    if sex=="Male": risk+=2
    return max(round(risk,1),1)

def framingham(age, tc, hdl, sbp, smoker):
    risk = (age*0.12)+(tc*0.02)-(hdl*0.03)+(sbp*0.015)
    if smoker: risk+=4
    return max(round(risk,1),1)

def qrisk_like(base, ethnicity, ckd, ra, fh, lp_a):
    adj=base
    if ethnicity=="South Asian": adj*=1.3
    if ckd: adj+=4
    if ra: adj+=3
    if fh: adj+=3
    if lp_a and lp_a>50: adj+=4
    return round(adj,1)

def risk_category(val):
    if val <5: return "Low"
    if val <7.5: return "Borderline"
    if val <20: return "Intermediate"
    return "High"

# =========================================================
# UI
# =========================================================
st.title("🫀 Comprehensive Cardiovascular Risk Assessment")

# PDF Upload
st.header("Upload Blood Report")
uploaded = st.file_uploader("Upload lab report PDF", type=["pdf"])

auto={}
if uploaded:
    auto=extract_labs(uploaded)
    st.success("Labs extracted — verify values below")

# DEMOGRAPHICS
st.header("Demographics")
c1,c2,c3 = st.columns(3)
age=c1.number_input("Age",20,90,45)
sex=c2.selectbox("Sex",["Male","Female"])
ethnicity=c3.selectbox("Ethnicity",["South Asian","White","Black","Other"])

# VITALS
st.header("Vitals")
c1,c2,c3,c4 = st.columns(4)
sbp=c1.number_input("Systolic BP",80,240,120)
dbp=c2.number_input("Diastolic BP",40,140,80)
height=c3.number_input("Height cm",120,210,170)
weight=c4.number_input("Weight kg",30,200,70)
waist=st.number_input("Waist circumference cm",50,150,90)

calc_bmi=bmi(height,weight)
if calc_bmi: st.info(f"BMI: {calc_bmi}")

# LABS
st.header("Standard Lipids")
c1,c2,c3,c4=st.columns(4)
tc=c1.number_input("Total Cholesterol",100,400, auto.get("tc",180))
hdl=c2.number_input("HDL",20,100, auto.get("hdl",45))
ldl=c3.number_input("LDL",30,300, auto.get("ldl",110))
tg=c4.number_input("Triglycerides",50,600, auto.get("tg",150))
hba1c=st.number_input("HbA1c",4.0,14.0, auto.get("hba1c",5.6))

# ADVANCED LIPIDS
st.header("Advanced Lipids")
c1,c2,c3=st.columns(3)
lp_a=c1.number_input("Lp(a) mg/dL",0,300, auto.get("lpa",10))
apob=c2.number_input("ApoB mg/dL",30,200, auto.get("apob",90))
apoa1=c3.number_input("ApoA1 mg/dL",50,250, auto.get("apoa1",140))

ratio=apo_ratio(apob,apoa1)
if ratio: st.success(f"ApoB/ApoA1 ratio: {ratio}")

# HISTORY
st.header("Medical History")
c1,c2=st.columns(2)
with c1:
    diabetes=st.checkbox("Diabetes")
    hypertension=st.checkbox("Hypertension")
    smoker=st.checkbox("Current smoker")
    fh=st.checkbox("Premature family history CAD")
with c2:
    mi=st.checkbox("Prior MI")
    stroke=st.checkbox("Stroke/TIA")
    pad=st.checkbox("Peripheral artery disease")
    ckd=st.checkbox("CKD ≥ stage 3")
    ra=st.checkbox("Rheumatoid arthritis")

# MEDICATIONS
st.header("Current Medications")
statin=st.checkbox("Currently on statin therapy")
dm_drugs=st.checkbox("On diabetes medications")
htn_drugs=st.checkbox("On hypertension medications")

# =========================================================
# CALCULATE
# =========================================================
if st.button("Calculate Risk"):

    ascvd_score=ascvd(age,sex,tc,hdl,sbp,smoker,diabetes)
    framingham_score=framingham(age,tc,hdl,sbp,smoker)
    qrisk_score=qrisk_like(ascvd_score,ethnicity,ckd,ra,fh,lp_a)

    st.header("Risk Scores")
    c1,c2,c3=st.columns(3)
    c1.metric("ASCVD 10yr Risk",f"{ascvd_score}% ({risk_category(ascvd_score)})")
    c2.metric("Framingham Risk",f"{framingham_score}% ({risk_category(framingham_score)})")
    c3.metric("QRISK-like Adjusted",f"{qrisk_score}% ({risk_category(qrisk_score)})")

    highest=max(ascvd_score,framingham_score,qrisk_score)

    st.header("Clinical Interpretation")

    if mi or stroke or pad:
        st.error("Established ASCVD → SECONDARY PREVENTION")
        st.write("LDL target <55 mg/dL")
        st.write("High-intensity statin mandatory")
        st.write("Add ezetimibe if LDL above goal → PCSK9 inhibitor if persistent")

    elif highest>=20:
        st.error("HIGH RISK PRIMARY PREVENTION")
        st.write("Start high-intensity statin")
        st.write("LDL target <70 mg/dL")

    elif highest>=7.5:
        st.warning("INTERMEDIATE RISK")
        st.write("Moderate-high intensity statin recommended")

    else:
        st.success("LOW RISK — lifestyle therapy")

    st.subheader("Exercise Prescription")
    st.write("Cardio: 150–300 min/week moderate intensity")
    st.write("Strength: 3 sessions/week full body")
    st.write("Daily steps goal: >8000")
