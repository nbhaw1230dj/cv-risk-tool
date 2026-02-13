import streamlit as st

st.set_page_config(layout="wide", page_title="🫀 Cardiovascular Risk Assessment Tool")

# ---------- helpers ----------

def na_number(container, label, default=0.0, minv=0.0, maxv=500.0, step=1.0, key=None):
    col1, col2 = container.columns([4,1])

    minv = float(minv)
    maxv = float(maxv)
    default = float(default)
    step = float(step)

    val = col1.number_input(
        label,
        min_value=minv,
        max_value=maxv,
        value=default,
        step=step,
        key=f"num_{label}_{key}"
    )

    na = col2.checkbox("NA", key=f"na_{label}_{key}")
    return None if na else float(val)

def bmi_calc(h,w):
    if h is not None and w is not None and h>0:
        return round(w/((h/100)**2),1)
    return None

def non_hdl(tc,hdl):
    if tc is not None and hdl is not None:
        return round(tc-hdl,1)
    return None

def ratio(a,b):
    if a is not None and b is not None and b>0:
        return round(a/b,2)
    return None

def percent_category(p):
    if p is None: return None
    if p<5: return "Low"
    if p<7.5: return "Moderate"
    if p<20: return "High"
    return "Very High"

def color(cat):
    return {
        "Low":"#4CAF50",
        "Moderate":"#FFC107",
        "High":"#FF9800",
        "Very High":"#F44336"
    }.get(cat,"#9E9E9E")


# ---------- UI ----------

st.title("🫀 Cardiovascular Risk Assessment Tool")

# DEMOGRAPHICS
st.header("Demographics")

age = na_number(st.container(), "Age", 40, 0, 100, key="age")

colA, colB, colC = st.columns(3)
sex = colA.selectbox("Sex",["Male","Female"])
eth = colB.selectbox("Ethnicity",["Indian","South Asian","White","Black","Other"])

height = na_number(colA, "Height (cm)",170,100,220,key="h")
weight = na_number(colB, "Weight (kg)",70,30,200,key="w")

bmi=bmi_calc(height,weight)
colC.metric("BMI", bmi if bmi is not None else "NA")


# VITALS
st.header("Vitals")
col1,col2 = st.columns(2)
sbp=na_number(col1,"SBP",120,70,240,key="sbp")
dbp=na_number(col2,"DBP",80,40,140,key="dbp")


# LIPIDS
st.header("Lipids")

r1c1,r1c2 = st.columns(2)
tc=na_number(r1c1,"Total Cholesterol",180,0,400,key="tc")
ldl=na_number(r1c2,"LDL-C",110,0,300,key="ldl")

r2c1,r2c2 = st.columns(2)
hdl=na_number(r2c1,"HDL-C",45,0,120,key="hdl")
tg=na_number(r2c2,"Triglycerides",150,0,600,key="tg")

nhdl=non_hdl(tc,hdl)
st.metric("Non-HDL", nhdl if nhdl is not None else "NA")

r3c1,r3c2 = st.columns(2)
apob=na_number(r3c1,"ApoB",90,0,200,key="apob")
apoa1=na_number(r3c2,"ApoA1",140,0,250,key="apoa1")

apo_ratio=ratio(apob,apoa1)
st.metric("ApoB/ApoA1 ratio", apo_ratio if apo_ratio is not None else "NA")

lpa=na_number(st.container(),"Lp(a)",10,0,300,key="lpa")


# DIABETES
st.header("Diabetes")
diabetes=st.radio("Diabetes",["No","Yes"])

if diabetes=="Yes":
    duration=na_number(st.container(),"Duration (years)",5,0,50,key="dm_dur")
    treatment=st.radio("Treatment",["Oral","Insulin"])
else:
    duration=None
    treatment=None


# SMOKING
st.header("Smoking")
smoke=st.selectbox("Smoking",["Never","Former","Current"])


# MEDICAL HISTORY
st.header("Medical History")
none_hist=st.checkbox("None of the above",key="hist_none")

mi=st.checkbox("MI",disabled=none_hist)
stroke=st.checkbox("Stroke/TIA",disabled=none_hist)
pad=st.checkbox("PAD",disabled=none_hist)
revasc=st.checkbox("Revascularization",disabled=none_hist)
ckd=st.checkbox("CKD",disabled=none_hist)
hf=st.checkbox("Heart failure",disabled=none_hist)
nafld=st.checkbox("NAFLD",disabled=none_hist)
mets=st.checkbox("Metabolic syndrome",disabled=none_hist)

ascvd = mi or stroke or pad or revasc


# FAMILY HISTORY
st.header("Family History")
st.write("Premature ASCVD = Male <55, Female <65")

none_fh=st.checkbox("None of the above",key="fh_none")
prem=st.checkbox("Premature ASCVD",disabled=none_fh)
fh_dm=st.checkbox("Diabetes",disabled=none_fh)
fh_htn=st.checkbox("Hypertension",disabled=none_fh)
fh_fh=st.checkbox("Familial Hypercholesterolemia",disabled=none_fh)


# MEDICATIONS
st.header("Medications")
none_med=st.checkbox("None of the above",key="med_none")

statin=st.checkbox("Statin",disabled=none_med)
antihtn=st.checkbox("Antihypertensive",disabled=none_med)
antidm=st.checkbox("Antidiabetic",disabled=none_med)
antiplate=st.checkbox("Antiplatelet",disabled=none_med)


# OFFICIAL CALCULATORS
st.header("Official Risk Calculators")
st.link_button("Open QRISK3 Calculator","https://qrisk.org/three/")
st.link_button("Open AHA PREVENT Calculator","https://professional.heart.org/en/guidelines-and-statements/prevent-calculator")

qrisk=na_number(st.container(),"QRISK3 %",10,0,100,key="qrisk")
aha=na_number(st.container(),"AHA ASCVD %",8,0,100,key="aha")
hf_risk=na_number(st.container(),"AHA HF %",3,0,100,key="hf")

qrisk_cat=percent_category(qrisk)
aha_cat=percent_category(aha)


# ---------- LAI ----------

risk_enhancers = (
    (smoke=="Current") or mets or fh_fh or
    (lpa is not None and lpa>50) or
    (apob is not None and apob>130)
)

if ascvd or ckd or (diabetes=="Yes" and duration is not None and duration>=10):
    lai="Very High"
elif diabetes=="Yes" or risk_enhancers:
    lai="High"
elif prem or fh_dm or fh_htn:
    lai="Moderate"
else:
    lai="Low"


# ---------- Visual Panel ----------

st.header("Risk Panel")
cols=st.columns(3)

for col,title,cat in zip(cols,["AHA","QRISK3","LAI"],[aha_cat,qrisk_cat,lai]):
    if cat:
        col.markdown(
            f"<div style='padding:20px;background:{color(cat)};color:white;border-radius:10px;text-align:center'>"
            f"<h3>{title}</h3><h2>{cat}</h2></div>",
            unsafe_allow_html=True
        )
    else:
        col.info(f"{title}: Unavailable")


# ---------- Unified Decision ----------

levels=["Low","Moderate","High","Very High"]
cats=[c for c in [aha_cat,qrisk_cat,lai] if c]

final = max(cats,key=lambda x:levels.index(x)) if cats else None

if final=="Moderate" and eth in ["Indian","South Asian"]:
    final="High"

if diabetes=="Yes" and apob is not None and apob>130 and final=="Moderate":
    final="High"


st.header("Statin Recommendation")

if final in ["High","Very High"]:
    st.success("Statins Recommended")
elif final:
    st.warning("Statins Not Mandatory")
else:
    st.info("Insufficient data")
