import streamlit as st
import math

st.set_page_config(layout="wide", page_title="🫀 Cardiovascular Risk Assessment Tool")

# Custom CSS for medical-grade UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Headers */
    h1 {
        color: #1a365d;
        font-weight: 600;
        border-bottom: 3px solid #2c5282;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #4299e1;
        padding-left: 1rem;
    }
    
    /* Risk panel cards */
    .risk-card {
        border-radius: 8px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%);
        border-left: 4px solid #ffc107;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fff3cd 0%, #ffd966 100%);
        border-left: 4px solid #ff9800;
    }
    
    .risk-veryhigh {
        background: linear-gradient(135deg, #f8d7da 0%, #f1b0b7 100%);
        border-left: 4px solid #dc3545;
    }
    
    .risk-unavailable {
        background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
        border-left: 4px solid #6c757d;
    }
    
    /* Contributing factors */
    .contributing-factors {
        background-color: rgba(255,255,255,0.7);
        border-radius: 6px;
        padding: 0.75rem;
        margin-top: 1rem;
        font-size: 0.9rem;
        border: 1px solid rgba(0,0,0,0.1);
    }
    
    .factor-title {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .factor-item {
        color: #4a5568;
        padding: 0.2rem 0;
        padding-left: 1rem;
        position: relative;
    }
    
    .factor-item:before {
        content: "•";
        position: absolute;
        left: 0;
        font-weight: bold;
    }
    
    /* Metrics */
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    /* Input fields */
    .stNumberInput > div > div > input {
        background-color: white;
        border: 1px solid #cbd5e0;
        border-radius: 4px;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2c5282;
        color: white;
        font-weight: 500;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #1a365d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #e6f3ff;
        border-left: 4px solid #4299e1;
        border-radius: 4px;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
    }
    
    /* Section dividers */
    hr {
        border: none;
        border-top: 2px solid #e2e8f0;
        margin: 2rem 0;
    }
    
    /* Checkbox labels */
    .stCheckbox label {
        font-weight: 500;
        color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

def na_number(container, label, default=None, minv=0.0, maxv=500.0, step=1.0, key=None):
    col1, col2 = container.columns([4,1])
    minv = float(minv)
    maxv = float(maxv)
    step = float(step)
    
    if default is None:
        default = minv
    else:
        default = float(default)
    
    val = col1.number_input(label, min_value=minv, max_value=maxv, value=default, step=step, key=f"num_{label}_{key}")
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
    return {"Low":"#4CAF50","Moderate":"#FFC107","High":"#FF9800","Very High":"#F44336"}.get(cat,"#9E9E9E")

def get_contributing_factors_aha(age, sex, tc, hdl, sbp, bp_treated, diabetes, smoking):
    """Identify main contributing factors for AHA PREVENT risk"""
    factors = []
    
    if age and age >= 65:
        factors.append("Advanced age (≥65 years)")
    elif age and age >= 55:
        factors.append("Age >55 years")
    
    if smoking == "Current":
        factors.append("Current smoking")
    
    if diabetes == "Yes":
        factors.append("Diabetes mellitus")
    
    if tc and tc >= 240:
        factors.append(f"High total cholesterol ({tc} mg/dL)")
    
    if hdl and hdl < 40:
        factors.append(f"Low HDL cholesterol ({hdl} mg/dL)")
    
    if sbp and sbp >= 160:
        factors.append(f"Severe hypertension (SBP {sbp} mmHg)")
    elif sbp and sbp >= 140:
        factors.append(f"Stage 2 hypertension (SBP {sbp} mmHg)")
    elif sbp and sbp >= 130:
        factors.append(f"Stage 1 hypertension (SBP {sbp} mmHg)")
    
    return factors

def get_contributing_factors_qrisk(age, sex, smoking, diabetes, bmi, sbp, tc_hdl_ratio, family_cvd, ckd, atrial_fib, rheumatoid_arthritis, ethnicity):
    """Identify main contributing factors for QRISK3"""
    factors = []
    
    if age and age >= 70:
        factors.append("Advanced age (≥70 years)")
    elif age and age >= 60:
        factors.append("Age ≥60 years")
    
    if smoking == "Current":
        factors.append("Current smoking")
    elif smoking == "Former":
        factors.append("Former smoking")
    
    if diabetes == "Yes":
        factors.append("Diabetes mellitus")
    
    if bmi and bmi >= 35:
        factors.append(f"Severe obesity (BMI {bmi:.1f})")
    elif bmi and bmi >= 30:
        factors.append(f"Obesity (BMI {bmi:.1f})")
    
    if sbp and sbp >= 160:
        factors.append(f"Severe hypertension (SBP {sbp} mmHg)")
    elif sbp and sbp >= 140:
        factors.append(f"Hypertension (SBP {sbp} mmHg)")
    
    if tc_hdl_ratio and tc_hdl_ratio >= 6:
        factors.append(f"High TC/HDL ratio ({tc_hdl_ratio:.1f})")
    elif tc_hdl_ratio and tc_hdl_ratio >= 5:
        factors.append(f"Elevated TC/HDL ratio ({tc_hdl_ratio:.1f})")
    
    if family_cvd:
        factors.append("Premature family history of CVD")
    
    if ckd:
        factors.append("Chronic kidney disease")
    
    if atrial_fib:
        factors.append("Atrial fibrillation")
    
    if rheumatoid_arthritis:
        factors.append("Rheumatoid arthritis")
    
    if ethnicity in ["Indian", "South Asian"]:
        factors.append("South Asian ethnicity")
    
    return factors

def get_contributing_factors_lai(ascvd, ckd, diabetes, duration, smoke, mets, fh_fh, lpa, apob, prem_ascvd, fh_dm, fh_htn, ldl):
    """Identify main contributing factors for LAI risk category"""
    factors = []
    
    if ascvd:
        factors.append("Established ASCVD (MI/Stroke/PAD/Revascularization)")
    
    if ckd:
        factors.append("Chronic kidney disease (stage 3-5)")
    
    if diabetes == "Yes":
        if duration and duration >= 10:
            factors.append(f"Long-standing diabetes ({int(duration)} years)")
        else:
            factors.append("Diabetes mellitus")
    
    if smoke == "Current":
        factors.append("Current smoking")
    
    if mets:
        factors.append("Metabolic syndrome")
    
    if fh_fh:
        factors.append("Familial hypercholesterolemia")
    
    if lpa and lpa >= 50:
        factors.append(f"Elevated Lp(a) ({lpa} mg/dL)")
    
    if apob and apob >= 130:
        factors.append(f"Elevated ApoB ({apob} mg/dL)")
    
    if ldl and ldl >= 190:
        factors.append(f"Severe hypercholesterolemia (LDL {ldl} mg/dL)")
    elif ldl and ldl >= 160:
        factors.append(f"High LDL cholesterol ({ldl} mg/dL)")
    
    if prem_ascvd:
        factors.append("Premature ASCVD in first-degree relatives")
    
    if fh_dm:
        factors.append("Family history of diabetes")
    
    if fh_htn:
        factors.append("Family history of hypertension")
    
    return factors

def calculate_qrisk3(age, sex, ethnicity, smoking, diabetes, height, weight, sbp, tc_hdl_ratio, antihtn, family_cvd, ckd, atrial_fib, rheumatoid_arthritis, migraine):
    required = [age, sex, tc_hdl_ratio, sbp]
    if None in required:
        return None
    if age < 25 or age > 84:
        return None
    bmi = bmi_calc(height, weight)
    if bmi is None:
        bmi = 25
    eth_code = {"Indian": 9,"South Asian": 9,"White": 1,"Black": 3,"Other": 1}.get(ethnicity, 1)
    smoke_code = {"Never": 0,"Former": 2,"Current": 4}.get(smoking, 0)
    is_female = sex == "Female"
    if is_female:
        survivor = 0.988876
        age_term = (age / 10) - 4.0
        smoking_param = smoke_code * 0.13
        diabetes_param = 0.86 if diabetes == "Yes" else 0
        bmi_param = 0.0
        if bmi >= 30:
            bmi_param = 0.56
        elif bmi >= 25:
            bmi_param = 0.23
        elif bmi >= 20:
            bmi_param = 0.12
        sbp_param = (sbp - 120) * 0.013
        tc_hdl_param = (tc_hdl_ratio - 4) * 0.15
        family_param = 0.45 if family_cvd else 0
        ckd_param = 0.60 if ckd else 0
        afib_param = 0.50 if atrial_fib else 0
        ra_param = 0.35 if rheumatoid_arthritis else 0
        score = age_term * 0.8 + smoking_param + diabetes_param + bmi_param + sbp_param + tc_hdl_param + family_param + ckd_param + afib_param + ra_param + (0.35 if eth_code == 9 else 0)
    else:
        survivor = 0.977268
        age_term = (age / 10) - 4.0
        smoking_param = smoke_code * 0.18
        diabetes_param = 0.59 if diabetes == "Yes" else 0
        bmi_param = 0.0
        if bmi >= 30:
            bmi_param = 0.48
        elif bmi >= 25:
            bmi_param = 0.20
        elif bmi >= 20:
            bmi_param = 0.10
        sbp_param = (sbp - 120) * 0.012
        tc_hdl_param = (tc_hdl_ratio - 4) * 0.17
        family_param = 0.54 if family_cvd else 0
        ckd_param = 0.65 if ckd else 0
        afib_param = 0.58 if atrial_fib else 0
        ra_param = 0.40 if rheumatoid_arthritis else 0
        score = age_term * 0.9 + smoking_param + diabetes_param + bmi_param + sbp_param + tc_hdl_param + family_param + ckd_param + afib_param + ra_param + (0.40 if eth_code == 9 else 0)
    risk_10yr = 100 * (1 - math.pow(survivor, math.exp(score)))
    return round(min(max(risk_10yr, 0), 100), 1)

def calculate_aha_prevent(age, sex, race, tc, hdl, sbp, bp_treated, diabetes, smoking):
    required = [age, sex, tc, hdl, sbp]
    if None in required:
        return None
    if age < 40 or age > 79:
        return None
    is_black = race in ["Black"]
    is_female = sex == "Female"
    ln_age = math.log(age)
    ln_tc = math.log(tc)
    ln_hdl = math.log(hdl)
    ln_sbp_treated = math.log(sbp) if bp_treated else 0
    ln_sbp_untreated = math.log(sbp) if not bp_treated else 0
    smoker = 1 if smoking == "Current" else 0
    dm = 1 if diabetes == "Yes" else 0
    if is_black and is_female:
        coef_ln_age = 17.114
        coef_ln_tc = 0.940
        coef_ln_hdl = -18.920
        coef_ln_age_hdl = 4.475
        coef_ln_treated_sbp = 29.291
        coef_ln_age_treated_sbp = -6.432
        coef_ln_untreated_sbp = 27.820
        coef_ln_age_untreated_sbp = -6.087
        coef_smoker = 0.691
        coef_dm = 0.874
        mean_sum = 86.61
        baseline_survival = 0.9533
        individual_sum = coef_ln_age * ln_age + coef_ln_tc * ln_tc + coef_ln_hdl * ln_hdl + coef_ln_age_hdl * ln_age * ln_hdl + coef_ln_treated_sbp * ln_sbp_treated + coef_ln_age_treated_sbp * ln_age * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated + coef_ln_age_untreated_sbp * ln_age * ln_sbp_untreated + coef_smoker * smoker + coef_dm * dm
    elif not is_black and is_female:
        coef_ln_age = -29.799
        coef_ln_age_sq = 4.884
        coef_ln_tc = 13.540
        coef_ln_age_tc = -3.114
        coef_ln_hdl = -13.578
        coef_ln_age_hdl = 3.149
        coef_ln_treated_sbp = 2.019
        coef_ln_untreated_sbp = 1.957
        coef_smoker = 7.574
        coef_ln_age_smoker = -1.665
        coef_dm = 0.661
        mean_sum = -29.18
        baseline_survival = 0.9665
        individual_sum = coef_ln_age * ln_age + coef_ln_age_sq * ln_age * ln_age + coef_ln_tc * ln_tc + coef_ln_age_tc * ln_age * ln_tc + coef_ln_hdl * ln_hdl + coef_ln_age_hdl * ln_age * ln_hdl + coef_ln_treated_sbp * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated + coef_smoker * smoker + coef_ln_age_smoker * ln_age * smoker + coef_dm * dm
    elif is_black and not is_female:
        coef_ln_age = 2.469
        coef_ln_tc = 0.302
        coef_ln_hdl = -0.307
        coef_ln_treated_sbp = 1.916
        coef_ln_untreated_sbp = 1.809
        coef_smoker = 0.549
        coef_dm = 0.645
        mean_sum = 19.54
        baseline_survival = 0.8954
        individual_sum = coef_ln_age * ln_age + coef_ln_tc * ln_tc + coef_ln_hdl * ln_hdl + coef_ln_treated_sbp * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated + coef_smoker * smoker + coef_dm * dm
    else:
        coef_ln_age = 12.344
        coef_ln_tc = 11.853
        coef_ln_age_tc = -2.664
        coef_ln_hdl = -7.990
        coef_ln_age_hdl = 1.769
        coef_ln_treated_sbp = 1.797
        coef_ln_untreated_sbp = 1.764
        coef_smoker = 7.837
        coef_ln_age_smoker = -1.795
        coef_dm = 0.658
        mean_sum = 61.18
        baseline_survival = 0.9144
        individual_sum = coef_ln_age * ln_age + coef_ln_tc * ln_tc + coef_ln_age_tc * ln_age * ln_tc + coef_ln_hdl * ln_hdl + coef_ln_age_hdl * ln_age * ln_hdl + coef_ln_treated_sbp * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated + coef_smoker * smoker + coef_ln_age_smoker * ln_age * smoker + coef_dm * dm
    risk_10yr = (1 - math.pow(baseline_survival, math.exp(individual_sum - mean_sum))) * 100
    return round(min(risk_10yr, 100), 1)

st.title("🫀 Cardiovascular Risk Assessment Tool")
st.markdown("*Evidence-based risk stratification for clinical decision support*")

st.header("Demographics")
age = na_number(st.container(), "Age", minv=0, maxv=100, key="age")
colA, colB, colC = st.columns(3)
sex = colA.selectbox("Sex",["Male","Female"])
eth = colB.selectbox("Ethnicity",["Indian","South Asian","White","Black","Other"])
height = na_number(colA, "Height (cm)", minv=100, maxv=220, key="h")
weight = na_number(colB, "Weight (kg)", minv=30, maxv=200, key="w")
bmi=bmi_calc(height,weight)
colC.metric("BMI", bmi if bmi is not None else "NA")

st.header("Vitals")
col1,col2 = st.columns(2)
sbp=na_number(col1,"SBP", minv=70, maxv=240, key="sbp")
dbp=na_number(col2,"DBP", minv=40, maxv=140, key="dbp")

st.header("Lipids")
r1c1,r1c2 = st.columns(2)
tc=na_number(r1c1,"Total Cholesterol", minv=0, maxv=400, key="tc")
ldl=na_number(r1c2,"LDL-C", minv=0, maxv=300, key="ldl")
r2c1,r2c2 = st.columns(2)
hdl=na_number(r2c1,"HDL-C", minv=0, maxv=120, key="hdl")
tg=na_number(r2c2,"Triglycerides", minv=0, maxv=600, key="tg")
nhdl=non_hdl(tc,hdl)
st.metric("Non-HDL", nhdl if nhdl is not None else "NA")
r3c1,r3c2 = st.columns(2)
apob=na_number(r3c1,"ApoB", minv=0, maxv=200, key="apob")
apoa1=na_number(r3c2,"ApoA1", minv=0, maxv=250, key="apoa1")
apo_ratio=ratio(apob,apoa1)
st.metric("ApoB/ApoA1 ratio", apo_ratio if apo_ratio is not None else "NA")
lpa=na_number(st.container(),"Lp(a)", minv=0, maxv=300, key="lpa")

st.header("Diabetes")
diabetes=st.radio("Diabetes",["No","Yes"])
if diabetes=="Yes":
    duration=na_number(st.container(),"Duration (years)", minv=0, maxv=50, key="dm_dur")
    treatment=st.radio("Treatment",["Oral","Insulin"])
else:
    duration=None
    treatment=None

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
atrial_fib=st.checkbox("Atrial fibrillation",disabled=none_hist)
rheumatoid_arthritis=st.checkbox("Rheumatoid arthritis",disabled=none_hist)
migraine=st.checkbox("Migraine",disabled=none_hist)
ascvd = mi or stroke or pad or revasc

st.header("Family History")
st.write("Premature ASCVD = Male <55, Female <65 in first-degree relatives")
none_fh=st.checkbox("None of the above",key="fh_none")
prem_ascvd=st.checkbox("Premature ASCVD in first-degree relatives",disabled=none_fh)
fh_dm=st.checkbox("Diabetes",disabled=none_fh)
fh_htn=st.checkbox("Hypertension",disabled=none_fh)
fh_fh=st.checkbox("Familial Hypercholesterolemia",disabled=none_fh)

st.header("Medications")
none_med=st.checkbox("None of the above",key="med_none")
statin=st.checkbox("Statin",disabled=none_med)
antihtn=st.checkbox("Antihypertensive",disabled=none_med)
antidm=st.checkbox("Antidiabetic",disabled=none_med)
antiplate=st.checkbox("Antiplatelet",disabled=none_med)

st.markdown("---")
st.header("📊 Calculated Risk Scores")

tc_hdl_ratio = ratio(tc, hdl)
qrisk = calculate_qrisk3(age, sex, eth, smoke, diabetes, height, weight, sbp, tc_hdl_ratio, antihtn, prem_ascvd, ckd, atrial_fib, rheumatoid_arthritis, migraine)
aha = calculate_aha_prevent(age, sex, eth, tc, hdl, sbp, antihtn, diabetes, smoke)

col1, col2 = st.columns(2)
with col1:
    if qrisk is not None:
        st.metric("QRISK3 (10-year CVD risk)", f"{qrisk}%")
    else:
        st.info("QRISK3: Not calculable (age 25-84 required, check inputs)")
with col2:
    if aha is not None:
        st.metric("AHA PREVENT (10-year ASCVD risk)", f"{aha}%")
    else:
        st.info("AHA PREVENT: Not calculable (age 40-79 required, check inputs)")

qrisk_cat = percent_category(qrisk)
aha_cat = percent_category(aha)

st.markdown("---")
st.subheader("🔗 Verify with Official Calculators")
col1, col2 = st.columns(2)
with col1:
    st.link_button("Open QRISK3 Calculator","https://qrisk.org/three/")
with col2:
    st.link_button("Open AHA PREVENT Calculator","https://professional.heart.org/en/guidelines-and-statements/prevent-calculator")

risk_enhancers = (smoke=="Current") or mets or fh_fh or (lpa is not None and lpa>50) or (apob is not None and apob>130)
if ascvd or ckd or (diabetes=="Yes" and duration is not None and duration>=10):
    lai="Very High"
elif diabetes=="Yes" or risk_enhancers:
    lai="High"
elif prem_ascvd or fh_dm or fh_htn:
    lai="Moderate"
else:
    lai="Low"

st.markdown("---")
st.header("🎯 Risk Stratification Panel")

cols=st.columns(3)

# AHA PREVENT
with cols[0]:
    if aha_cat:
        cat_class = aha_cat.lower().replace(" ", "")
        st.markdown(f'<div class="risk-card risk-{cat_class}"><h3 style="margin:0; color:#2d3748;">AHA PREVENT</h3><h1 style="margin:0.5rem 0; color:#1a365d;">{aha_cat}</h1><p style="margin:0; font-size:1.2rem; font-weight:600;">{aha}%</p></div>', unsafe_allow_html=True)
        
        if aha_cat != "Low":
            factors = get_contributing_factors_aha(age, sex, tc, hdl, sbp, antihtn, diabetes, smoke)
            if factors:
                st.markdown('<div class="contributing-factors"><div class="factor-title">Contributing Factors:</div>', unsafe_allow_html=True)
                for factor in factors[:5]:
                    st.markdown(f'<div class="factor-item">{factor}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="risk-card risk-unavailable"><h3 style="margin:0;">AHA PREVENT</h3><p style="margin:0.5rem 0;">Not calculable</p></div>', unsafe_allow_html=True)

# QRISK3
with cols[1]:
    if qrisk_cat:
        cat_class = qrisk_cat.lower().replace(" ", "")
        st.markdown(f'<div class="risk-card risk-{cat_class}"><h3 style="margin:0; color:#2d3748;">QRISK3</h3><h1 style="margin:0.5rem 0; color:#1a365d;">{qrisk_cat}</h1><p style="margin:0; font-size:1.2rem; font-weight:600;">{qrisk}%</p></div>', unsafe_allow_html=True)
        
        if qrisk_cat != "Low":
            factors = get_contributing_factors_qrisk(age, sex, smoke, diabetes, bmi, sbp, tc_hdl_ratio, prem_ascvd, ckd, atrial_fib, rheumatoid_arthritis, eth)
            if factors:
                st.markdown('<div class="contributing-factors"><div class="factor-title">Contributing Factors:</div>', unsafe_allow_html=True)
                for factor in factors[:5]:
                    st.markdown(f'<div class="factor-item">{factor}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="risk-card risk-unavailable"><h3 style="margin:0;">QRISK3</h3><p style="margin:0.5rem 0;">Not calculable</p></div>', unsafe_allow_html=True)

# LAI
with cols[2]:
    if lai:
        cat_class = lai.lower().replace(" ", "")
        st.markdown(f'<div class="risk-card risk-{cat_class}"><h3 style="margin:0; color:#2d3748;">LAI Risk</h3><h1 style="margin:0.5rem 0; color:#1a365d;">{lai}</h1><p style="margin:0; font-size:0.9rem; font-style:italic;">Lipid Association of India</p></div>', unsafe_allow_html=True)
        
        if lai != "Low":
            factors = get_contributing_factors_lai(ascvd, ckd, diabetes, duration, smoke, mets, fh_fh, lpa, apob, prem_ascvd, fh_dm, fh_htn, ldl)
            if factors:
                st.markdown('<div class="contributing-factors"><div class="factor-title">Contributing Factors:</div>', unsafe_allow_html=True)
                for factor in factors[:5]:
                    st.markdown(f'<div class="factor-item">{factor}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="risk-card risk-unavailable"><h3 style="margin:0;">LAI Risk</h3><p style="margin:0.5rem 0;">Unavailable</p></div>', unsafe_allow_html=True)

st.markdown("---")

levels=["Low","Moderate","High","Very High"]
cats=[c for c in [aha_cat,qrisk_cat,lai] if c]
final = max(cats,key=lambda x:levels.index(x)) if cats else None
if final=="Moderate" and eth in ["Indian","South Asian"]:
    final="High"
if diabetes=="Yes" and apob is not None and apob>130 and final=="Moderate":
    final="High"

st.header("💊 Statin Recommendation")
if final in ["High","Very High"]:
    st.success("✅ **Statins Recommended** — High or Very High cardiovascular risk identified")
elif final:
    st.warning("⚠️ **Statins Not Mandatory** — Consider lifestyle modification and re-assessment")
else:
    st.info("ℹ️ **Insufficient Data** — Complete required fields for risk assessment")
