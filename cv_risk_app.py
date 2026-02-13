import streamlit as st

st.set_page_config(layout="wide", page_title="🫀 Cardiovascular Risk Assessment Tool")

# ----- helpers -----

def na_number(label, default=0.0, minv=0.0, maxv=500.0, step=1.0, key=None):
c1,c2=st.columns([4,1])
val=c1.number_input(label,min_value=minv,max_value=maxv,value=default,step=step,key=f"num_{label}{key}")
na=c2.checkbox("NA",key=f"na{label}_{key}")
return None if na else val

def bmi_calc(h,w):
if h and w and h>0: return round(w/((h/100)**2),1)
return None

def non_hdl(tc,hdl):
if tc is not None and hdl is not None: return round(tc-hdl,1)
return None

def ratio(a,b):
if a and b and b>0: return round(a/b,2)
return None

def percent_category(p):
if p is None: return None
if p<5: return "Low"
if p<7.5: return "Moderate"
if p<20: return "High"
return "Very High"

def color(cat):
return {"Low":"#4CAF50","Moderate":"#FFC107","High":"#FF9800","Very High":"#F44336"}.get(cat,"#9E9E9E")

----- UI -----

st.title("🫀 Cardiovascular Risk Assessment Tool")

st.header("Demographics")
age=na_number("Age",40,0,100,key="age")
sex=st.selectbox("Sex",["Male","Female"])
eth=st.selectbox("Ethnicity",["Indian","South Asian","White","Black","Other"])
height=na_number("Height (cm)",170,100,220,key="h")
weight=na_number("Weight (kg)",70,30,200,key="w")
bmi=bmi_calc(height,weight)
st.write(f"BMI: {bmi if bmi else ‘NA'}")

st.header("Vitals")
sbp=na_number("SBP",120,70,240,key="sbp")
dbp=na_number("DBP",80,40,140,key="dbp")

st.header("Lipids")
tc=na_number("Total Cholesterol",180,0,400,key="tc")
ldl=na_number("LDL-C",110,0,300,key="ldl")
hdl=na_number("HDL-C",45,0,120,key="hdl")
tg=na_number("Triglycerides",150,0,600,key="tg")
nhdl=non_hdl(tc,hdl)
st.write(f"Non-HDL: {nhdl if nhdl else ‘NA'}")
apob=na_number("ApoB",90,0,200,key="apob")
apoa1=na_number("ApoA1",140,0,250,key="apoa1")
apo_ratio=ratio(apob,apoa1)
st.write(f"ApoB/ApoA1 ratio: {apo_ratio if apo_ratio else ‘NA'}")
lpa=na_number("Lp(a)",10,0,300,key="lpa")

st.header("Diabetes")
diabetes=st.radio("Diabetes",["No","Yes"])
duration=na_number("Duration (years)",5,0,50,key="dm_dur") if diabetes=="Yes" else None
treatment=st.radio("Treatment",["Oral","Insulin"]) if diabetes=="Yes" else None

st.header("Smoking")
smoke=st.selectbox("Smoking",["Never","Former","Current"])

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
ascvd=mi or stroke or pad or revasc

st.header("Family History")
st.write("Premature ASCVD = Male <55, Female <65")
none_fh=st.checkbox("None of the above",key="fh_none")
prem=st.checkbox("Premature ASCVD",disabled=none_fh)
fh_dm=st.checkbox("Diabetes",disabled=none_fh)
fh_htn=st.checkbox("Hypertension",disabled=none_fh)
fh_fh=st.checkbox("Familial Hypercholesterolemia",disabled=none_fh)

st.header("Medications")
none_med=st.checkbox("None of the above",key="med_none")
statin=st.checkbox("Statin",disabled=none_med)
antihtn=st.checkbox("Antihypertensive",disabled=none_med)
antidm=st.checkbox("Antidiabetic",disabled=none_med)
antiplate=st.checkbox("Antiplatelet",disabled=none_med)

st.header("Official Risk Calculators")
st.link_button("Open QRISK3 Calculator","https://qrisk.org/three/")
st.link_button("Open AHA PREVENT Calculator","https://professional.heart.org/en/guidelines-and-statements/prevent-calculator")

qrisk=na_number("QRISK3 %",10,0,100,key="qrisk")
aha=na_number("AHA ASCVD %",8,0,100,key="aha")
hf_risk=na_number("AHA HF %",3,0,100,key="hf")

qrisk_cat=percent_category(qrisk)
aha_cat=percent_category(aha)

----- LAI -----

risk_enhancers = (smoke=="Current") or mets or fh_fh or (lpa and lpa>50) or (apob and apob>130)

if ascvd or ckd or (diabetes=="Yes" and duration and duration>=10):
lai="Very High"
elif diabetes=="Yes" or risk_enhancers:
lai="High"
elif prem or fh_dm or fh_htn:
lai="Moderate"
else:
lai="Low"

----- Visual Panel -----

st.header("Risk Panel")
cols=st.columns(3)
for col,title,cat in zip(cols,["AHA","QRISK3","LAI"],[aha_cat,qrisk_cat,lai]):
col.markdown(f"{title}{cat if cat else ‘Unavailable'}",unsafe_allow_html=True)

----- Unified Decision -----

levels=["Low","Moderate","High","Very High"]
cats=[c for c in [aha_cat,qrisk_cat,lai] if c]
final=max(cats,key=lambda x:levels.index(x)) if cats else None

if eth in ["Indian","South Asian"] and final=="Moderate":
final="High"

if diabetes=="Yes" and apob and apob>130 and final=="Moderate":
final="High"

st.header("Statin Recommendation")
if final in ["High","Very High"]:
st.success("Statins Recommended")
elif final:
st.warning("Statins Not Mandatory")
else:
st.info("Insufficient data")
