import streamlit as st

st.set_page_config(layout="wide", page_title="Cardiovascular Risk Decision Support")

# -------------------------
# Helpers
# -------------------------
def safe_float(x):
    try:
        if x is None or x == "":
            return None
        return float(x)
    except:
        return None

def bmi_calc(h, w):
    if h and w and h>0:
        return round(w/((h/100)**2),1)
    return None

def non_hdl(tc, hdl):
    if tc is not None and hdl is not None:
        return tc - hdl
    return None

def apo_ratio(apob, apoa1):
    if apob and apoa1 and apoa1>0:
        return round(apob/apoa1,2)
    return None

def category_from_percent(p):
    if p is None: return None
    if p < 5: return "Low"
    if p < 7.5: return "Moderate"
    if p < 20: return "High"
    return "Very High"

def color_for_category(cat):
    return {
        "Low":"#4CAF50",
        "Moderate":"#FFC107",
        "High":"#FF9800",
        "Very High":"#F44336"
    }.get(cat,"#9E9E9E")

# -------------------------
# LAI Rule Logic
# -------------------------
def lai_category(data):
    if data["ascvd_history"]:
        return "Very High"

    if data["ckd"]:
        return "Very High"

    if data["diabetes"] and data["diabetes_duration"]>=10:
        return "Very High"

    if data["diabetes"]:
        return "High"

    if data["lp_a"] and data["lp_a"]>50:
        return "High"

    if data["apob"] and data["apob"]>=130:
        return "High"

    if data["risk_factors"]>=2:
        return "Moderate"

    return "Low"

# -------------------------
# UI INPUTS
# -------------------------
st.title("Cardiovascular Risk Decision Support")

st.header("Demographics")
c1,c2,c3 = st.columns(3)
age=c1.number_input("Age",0,100,40)
sex=c2.selectbox("Sex",["Male","Female"])
eth=c3.selectbox("Ethnicity",["South Asian","Other"])

c1,c2=st.columns(2)
height=c1.number_input("Height (cm)",100,220,170)
weight=c2.number_input("Weight (kg)",30,200,70)
bmi=bmi_calc(height,weight)
st.write(f"BMI: {bmi if bmi else 'N/A'}")

st.header("Vitals")
sbp=st.number_input("SBP",80,240,120)
dbp=st.number_input("DBP",40,140,80)

st.header("Lipids")
c1,c2,c3,c4=st.columns(4)
tc=c1.number_input("Total Cholesterol",0,400,180)
ldl=c2.number_input("LDL",0,300,110)
hdl=c3.number_input("HDL",0,120,45)
tg=c4.number_input("Triglycerides",0,600,150)

nhdl=non_hdl(tc,hdl)
st.write(f"Non-HDL: {nhdl if nhdl else 'N/A'}")

c1,c2,c3=st.columns(3)
apob=c1.number_input("ApoB",0,200,90)
apoa1=c2.number_input("ApoA1",0,250,140)
lpa=c3.number_input("Lp(a)",0,300,10)

ratio=apo_ratio(apob,apoa1)
st.write(f"ApoB/ApoA1 ratio: {ratio if ratio else 'N/A'}")

st.header("Diabetes")
diabetes=st.checkbox("Diabetes")
diabetes_duration=st.number_input("Duration (years)",0,40,0)
dm_tx=st.checkbox("On treatment")

st.header("Smoking")
smoke=st.selectbox("Smoking",["Never","Former","Current"])

st.header("Medical History")
c1,c2=st.columns(2)
mi=c1.checkbox("MI")
stroke=c1.checkbox("Stroke/TIA")
pad=c1.checkbox("PAD")
revasc=c1.checkbox("Revascularization")

ckd=c2.checkbox("CKD")
hf=c2.checkbox("Heart Failure")
nafld=c2.checkbox("NAFLD")
mets=c2.checkbox("Metabolic Syndrome")

ascvd_history = mi or stroke or pad or revasc

st.header("Family History")
fh=st.checkbox("Premature ASCVD")

st.header("Medications")
statin=st.checkbox("Statin")
antihtn=st.checkbox("Antihypertensive")
antidm=st.checkbox("Antidiabetic")
antiplatelet=st.checkbox("Antiplatelet")

st.header("Official Risk Calculator Results")
qrisk=safe_float(st.text_input("QRISK3 (%)"))
aha=safe_float(st.text_input("AHA ASCVD (%)"))
hf_risk=safe_float(st.text_input("AHA Heart Failure (%)"))

# -------------------------
# PROCESS
# -------------------------
risk_factors=sum([smoke=="Current", fh, hdl<40 if hdl else False])

lai=lai_category({
    "ascvd_history":ascvd_history,
    "ckd":ckd,
    "diabetes":diabetes,
    "diabetes_duration":diabetes_duration,
    "lp_a":lpa,
    "apob":apob,
    "risk_factors":risk_factors
})

aha_cat=category_from_percent(aha)
qrisk_cat=category_from_percent(qrisk)

# -------------------------
# VISUAL PANEL
# -------------------------
st.header("Risk Panel")

cols=st.columns(3)

for col,title,cat in zip(cols,["AHA","QRISK3","LAI"],[aha_cat,qrisk_cat,lai]):
    color=color_for_category(cat)
    col.markdown(
        f"""
        <div style='padding:20px;border-radius:10px;background:{color};color:white;text-align:center'>
        <h3>{title}</h3>
        <h2>{cat if cat else 'Insufficient data'}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# INTERPRETATION
# -------------------------
st.header("Guideline Interpretation")

with st.expander("AHA Recommendation"):
    if aha_cat=="Very High":
        st.write("High intensity statin indicated")
    elif aha_cat=="High":
        st.write("Moderate to high intensity statin")
    elif aha_cat=="Moderate":
        st.write("Consider statin based on risk discussion")
    else:
        st.write("Lifestyle management")

with st.expander("QRISK3 Recommendation"):
    if qrisk_cat in ["High","Very High"]:
        st.write("Offer statin therapy")
    else:
        st.write("Lifestyle first")

with st.expander("LAI Recommendation"):
    if lai=="Very High":
        st.write("LDL target <55 mg/dL. Add ezetimibe ± PCSK9")
    elif lai=="High":
        st.write("LDL target <70 mg/dL. High intensity statin")
    elif lai=="Moderate":
        st.write("LDL target <100 mg/dL")
    else:
        st.write("Lifestyle therapy")

# -------------------------
# UNIFIED DECISION
# -------------------------
st.header("Unified Clinical Plan")

levels=["Low","Moderate","High","Very High"]
max_level=max([aha_cat,qrisk_cat,lai], key=lambda x: levels.index(x) if x else 0)

st.write(f"Final Risk Category: {max_level}")

if max_level=="Very High":
    st.write("- High intensity statin")
    st.write("- Add ezetimibe")
    st.write("- Consider PCSK9")

elif max_level=="High":
    st.write("- Moderate/high statin")

elif max_level=="Moderate":
    st.write("- Consider statin")

else:
    st.write("- Lifestyle only")

st.write("Lifestyle:")
st.write("- Aerobic 150–300 min/week")
st.write("- Resistance 2–3 sessions/week")
