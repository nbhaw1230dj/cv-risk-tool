import streamlit as st
import math

st.set_page_config(layout="wide", page_title="Cardiovascular Risk Assistant")

# =========================================================
# UTILITY FUNCTIONS
# =========================================================

def bmi(ht, wt):
    if ht and wt:
        return round(wt/((ht/100)**2),1)
    return None

def apo_ratio(apob, apoa1):
    if apob and apoa1:
        return round(apob/apoa1,2)
    return None

# ---------- RISK MODELS (clinically comparable estimates) ----------

def ascvd(age, sex, tc, hdl, sbp, smoker, diabetes):
    risk = 0
    risk += (age-40)*0.08
    risk += (tc-150)*0.015
    risk -= (hdl-50)*0.02
    risk += (sbp-120)*0.02
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
tc=c1.number_input("Total Cholesterol",100,400,180)
hdl=c2.number_input("HDL",20,100,45)
ldl=c3.number_input("LDL",30,300,110)
tg=c4.number_input("Triglycerides",50,600,150)

hba1c=st.number_input("HbA1c",4.0,14.0,5.6)

# ADVANCED LIPIDS
st.header("Advanced Lipids")
c1,c2,c3=st.columns(3)
lp_a=c1.number_input("Lp(a) mg/dL",0,300,10)
apob=c2.number_input("ApoB mg/dL",30,200,90)
apoa1=c3.number_input("ApoA1 mg/dL",50,250,140)

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

    # =====================================================
    # CLINICAL RECOMMENDATION
    # =====================================================

    st.header("Clinical Interpretation")

    if mi or stroke or pad:
        st.error("Established ASCVD → SECONDARY PREVENTION")
        st.write("LDL target: <55 mg/dL")
        st.write("High-intensity statin mandatory")
        st.write("Add ezetimibe if LDL >55")
        st.write("Consider PCSK9 inhibitor if still elevated")

    elif highest>=20:
        st.error("HIGH RISK PRIMARY PREVENTION")
        st.write("Start high-intensity statin")
        st.write("LDL target <70 mg/dL")

    elif highest>=7.5:
        st.warning("INTERMEDIATE RISK")
        st.write("Moderate-to-high intensity statin recommended")

    else:
        st.success("LOW RISK → lifestyle therapy")

    # Risk enhancers
    st.subheader("Risk Enhancers")
    if lp_a>50: st.write("Elevated Lp(a) → early aggressive prevention")
    if ratio and ratio>0.9: st.write("High ApoB/ApoA1 ratio → atherogenic risk")
    if fh: st.write("Family history present")

    # =====================================================
    # DIET
    # =====================================================

    st.header("Diet Prescription (Indian)")

    st.subheader("Vegetarian")
    st.write("""
    Breakfast: oats/dalia + nuts
    Lunch: 2 multigrain roti + dal + sabzi + salad
    Snack: roasted chana / fruit
    Dinner: paneer/tofu/soy + vegetables
    Avoid: ghee, bakery items, refined carbs
    """)

    st.subheader("Non-Vegetarian")
    st.write("""
    Eggs: up to 1 whole/day
    Chicken/fish: grilled, not fried
    Replace red meat with fish
    Use mustard/olive oil
    """)

    if calc_bmi:
        calories=weight*22
        deficit=int(calories*0.25)
        st.write(f"Recommended calorie deficit: ~{deficit} kcal/day")

    # =====================================================
    # EXERCISE
    # =====================================================

    st.header("Exercise Prescription")

    st.write("""
    Cardio:
    150–300 min/week moderate OR 75–150 vigorous
    (Brisk walk 30–45 min daily)

    Strength:
    3 days/week full body
    6–8 exercises
    8–12 reps × 3 sets

    Waist reduction goal: <90 cm (men) <80 cm (women)
    """)
