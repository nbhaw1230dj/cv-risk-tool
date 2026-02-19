import streamlit as st
import math

st.set_page_config(
    layout="wide",
    page_title="Cardiovascular Risk Assessment",
    initial_sidebar_state="collapsed"
)

# ========== THEME MANAGEMENT ==========
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

def reset_all():
    preserve = {"theme"}
    keys_to_delete = [k for k in st.session_state.keys() if k not in preserve]
    for k in keys_to_delete:
        del st.session_state[k]

is_dark = st.session_state.theme == "dark"

# ========== THEME VARIABLES ==========
if is_dark:
    BG_PAGE        = "#0f1117"
    BG_SECONDARY   = "#1a1d27"
    BG_INPUT       = "#252836"
    TEXT_PRIMARY   = "#e8eaf0"
    TEXT_SECONDARY = "#9aa0b8"
    TEXT_MUTED     = "#6b7280"
    BORDER_COLOR   = "#2e3347"
    ACCENT         = "#4c9ef8"
    ACCENT_DARK    = "#3a82d6"
    HEADING_COLOR  = "#e8eaf0"
    H2_LEFT_BAR    = "#4c9ef8"
    H2_BG          = "rgba(76, 158, 248, 0.08)"
    DIVIDER        = "#2e3347"
    METRIC_BG      = "#1e2130"
    METRIC_VAL     = "#e8eaf0"
    BTN_BG         = "#3a82d6"
    BTN_HOVER      = "#2d6dbf"
    INFO_BG        = "rgba(76, 158, 248, 0.1)"
    INFO_BORDER    = "#4c9ef8"
    WARN_BG        = "rgba(255, 193, 7, 0.1)"
    WARN_BORDER    = "#ffc107"
    TOOLBAR_BG     = "#13161f"
    TOOLBAR_BORDER = "#2e3347"
    RISK_LOW_BG       = "linear-gradient(135deg, #1a3326 0%, #1f3d2e 100%)"
    RISK_LOW_BORDER   = "#28a745"
    RISK_MOD_BG       = "linear-gradient(135deg, #2e2910 0%, #3a3412 100%)"
    RISK_MOD_BORDER   = "#ffc107"
    RISK_HIGH_BG      = "linear-gradient(135deg, #2e1f0a 0%, #3a2710 100%)"
    RISK_HIGH_BORDER  = "#ff9800"
    RISK_VH_BG        = "linear-gradient(135deg, #2e1118 0%, #3a1520 100%)"
    RISK_VH_BORDER    = "#dc3545"
    RISK_NA_BG        = "linear-gradient(135deg, #1a1d27 0%, #252836 100%)"
    RISK_NA_BORDER    = "#4a5568"
    CF_BG             = "rgba(255,255,255,0.04)"
    CF_BORDER         = "rgba(255,255,255,0.08)"
    CF_TITLE          = "#9aa0b8"
    CF_ITEM           = "#9aa0b8"
    CF_BULLET         = "#4c9ef8"
    TOGGLE_ICON       = "☀"
    SELECTBOX_COLOR   = "#e8eaf0"
    INPUT_COLOR       = "#e8eaf0"
    CAPTION_COLOR     = "#9aa0b8"
    TAB_BG            = "#1a1d27"
    TAB_ACTIVE_BG     = "#252836"
    TAB_COLOR         = "#9aa0b8"
    TAB_ACTIVE_COLOR  = "#4c9ef8"
    TAB_ACTIVE_BORDER = "#4c9ef8"
    UNIT_COLOR        = "#6b7280"
    TOOLBAR_BTN_BG    = "#2a2f45"
    TOOLBAR_BTN_BORDER= "#4c9ef8"
    TOOLBAR_BTN_COLOR = "#e8eaf0"
    SECTION_LABEL_COLOR = "#4c9ef8"
    # Dark mode button specifics
    RESET_BTN_BG      = "#2a2f45"
    RESET_BTN_COLOR   = "#e8eaf0"
    RESET_BTN_BORDER  = "#6b7a9e"
    THEME_BTN_BG      = "#4c9ef8"
    THEME_BTN_COLOR   = "#ffffff"
    THEME_BTN_BORDER  = "#4c9ef8"
else:
    BG_PAGE        = "#f0f2f6"
    BG_SECONDARY   = "#ffffff"
    BG_INPUT       = "#ffffff"
    TEXT_PRIMARY   = "#1a202c"
    TEXT_SECONDARY = "#4a5568"
    TEXT_MUTED     = "#718096"
    BORDER_COLOR   = "#dde1e9"
    ACCENT         = "#2563eb"
    ACCENT_DARK    = "#1e40af"
    HEADING_COLOR  = "#0f172a"
    H2_LEFT_BAR    = "#2563eb"
    H2_BG          = "rgba(37, 99, 235, 0.06)"
    DIVIDER        = "#e2e8f0"
    METRIC_BG      = "#ffffff"
    METRIC_VAL     = "#0f172a"
    BTN_BG         = "#2563eb"
    BTN_HOVER      = "#1e40af"
    INFO_BG        = "#eff6ff"
    INFO_BORDER    = "#2563eb"
    WARN_BG        = "#fffbeb"
    WARN_BORDER    = "#f59e0b"
    TOOLBAR_BG     = "#ffffff"
    TOOLBAR_BORDER = "#dde1e9"
    RISK_LOW_BG       = "linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%)"
    RISK_LOW_BORDER   = "#16a34a"
    RISK_MOD_BG       = "linear-gradient(135deg, #fefce8 0%, #fef08a 100%)"
    RISK_MOD_BORDER   = "#ca8a04"
    RISK_HIGH_BG      = "linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%)"
    RISK_HIGH_BORDER  = "#ea580c"
    RISK_VH_BG        = "linear-gradient(135deg, #fff1f2 0%, #fecdd3 100%)"
    RISK_VH_BORDER    = "#dc2626"
    RISK_NA_BG        = "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)"
    RISK_NA_BORDER    = "#94a3b8"
    CF_BG             = "rgba(255,255,255,0.9)"
    CF_BORDER         = "rgba(0,0,0,0.07)"
    CF_TITLE          = "#374151"
    CF_ITEM           = "#4b5563"
    CF_BULLET         = "#2563eb"
    TOGGLE_ICON       = "🌙"
    SELECTBOX_COLOR   = "#1a202c"
    INPUT_COLOR       = "#1a202c"
    CAPTION_COLOR     = "#64748b"
    TAB_BG            = "#f1f5f9"
    TAB_ACTIVE_BG     = "#ffffff"
    TAB_COLOR         = "#64748b"
    TAB_ACTIVE_COLOR  = "#1e40af"
    TAB_ACTIVE_BORDER = "#2563eb"
    UNIT_COLOR        = "#94a3b8"
    TOOLBAR_BTN_BG    = "#f8fafc"
    TOOLBAR_BTN_BORDER= "#dde1e9"
    TOOLBAR_BTN_COLOR = "#475569"
    SECTION_LABEL_COLOR = "#2563eb"
    # Light mode button specifics
    RESET_BTN_BG      = "#ffffff"
    RESET_BTN_COLOR   = "#374151"
    RESET_BTN_BORDER  = "#d1d5db"
    THEME_BTN_BG      = "#2563eb"
    THEME_BTN_COLOR   = "#ffffff"
    THEME_BTN_BORDER  = "#2563eb"

# ========== INJECT CSS ==========
st.markdown(f"""
<style>

/* Remove Streamlit top chrome completely */
header, footer, #MainMenu, .stDeployButton,
[data-testid="stToolbar"] {{
    display: none !important;
}}

html, body, .stApp {{
    background-color: {BG_PAGE} !important;
}}

[data-testid="stAppViewContainer"] {{
    background-color: {BG_PAGE} !important;
}}

.block-container {{
    padding-top: 3.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}}

/* Title */
.main-title {{
    font-size: clamp(1.9rem, 3.2vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    color: {TEXT_PRIMARY};
    border-bottom: 3px solid {ACCENT};
    padding-bottom: 0.6rem;
    margin-bottom: 1.4rem;
}}

/* Section labels */
.section-sep-label {{
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {ACCENT};
}}

.section-sep-line {{
    height: 1px;
    background: {BORDER_COLOR};
    flex: 1;
}}

.section-sep {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 0.9rem 0;
}}

/* Buttons */
.stButton > button {{
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.2rem !important;
}}

.cv-reset-btn .stButton > button {{
    background-color: {RESET_BTN_BG} !important;
    color: {RESET_BTN_COLOR} !important;
    border: 1.5px solid {RESET_BTN_BORDER} !important;
}}

.cv-theme-btn .stButton > button {{
    background-color: {THEME_BTN_BG} !important;
    color: {THEME_BTN_COLOR} !important;
    border: 1.5px solid {THEME_BTN_BORDER} !important;
}}

input, select, textarea {{
    background-color: {BG_INPUT} !important;
    color: {TEXT_PRIMARY} !important;
    border: 1.5px solid {BORDER_COLOR} !important;
    border-radius: 6px !important;
}}

[data-testid="stMetric"] {{
    background: {BG_SECONDARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    padding: 1rem;
}}

[data-testid="stMetricValue"] {{
    font-size: 1.6rem !important;
    font-weight: 800 !important;
}}

.cv-ref-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    background: {BG_SECONDARY};
    color: {TEXT_SECONDARY} !important;
    border: 1.5px solid {BORDER_COLOR};
    text-decoration: none !important;
}}

.cv-ref-pill:hover {{
    border-color: {ACCENT};
    color: {ACCENT} !important;
}}

</style>
""", unsafe_allow_html=True)


# ========== HELPER FUNCTIONS ==========

def opt_num(container, label, minv=0.0, maxv=9999.0, step=1.0, key=None, fmt="%.0f"):
    minv = float(minv)
    maxv = float(maxv)
    step = float(step)
    val = container.number_input(
        label,
        min_value=minv,
        max_value=maxv,
        value=None,
        step=step,
        format=fmt,
        placeholder="—",
        key=key
    )
    return val


def bmi_calc(h, w):
    if h is not None and w is not None and h > 0:
        return round(w / ((h / 100) ** 2), 1)
    return None


def non_hdl(tc, hdl):
    if tc is not None and hdl is not None:
        return round(tc - hdl, 1)
    return None


def ratio(a, b):
    if a is not None and b is not None and b > 0:
        return round(a / b, 2)
    return None


def percent_category(p):
    if p is None:
        return None
    if p < 5:
        return "Low"
    if p < 7.5:
        return "Moderate"
    if p < 20:
        return "High"
    return "Very High"


def get_contributing_factors_aha(age, sex, tc, hdl, sbp, bp_treated, diabetes, smoking):
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
        factors.append(f"High total cholesterol ({tc:.0f} mg/dL)")
    if hdl and hdl < 40:
        factors.append(f"Low HDL cholesterol ({hdl:.0f} mg/dL)")
    if sbp and sbp >= 160:
        factors.append(f"Severe hypertension (SBP {sbp:.0f} mmHg)")
    elif sbp and sbp >= 140:
        factors.append(f"Stage 2 hypertension (SBP {sbp:.0f} mmHg)")
    elif sbp and sbp >= 130:
        factors.append(f"Stage 1 hypertension (SBP {sbp:.0f} mmHg)")
    return factors


def get_contributing_factors_qrisk(age, sex, smoking, diabetes, bmi, sbp, tc_hdl_ratio, family_cvd, ckd, atrial_fib, rheumatoid_arthritis, ethnicity):
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
        factors.append(f"Severe hypertension (SBP {sbp:.0f} mmHg)")
    elif sbp and sbp >= 140:
        factors.append(f"Hypertension (SBP {sbp:.0f} mmHg)")
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
        factors.append(f"Elevated Lp(a) ({lpa:.0f} mg/dL)")
    if apob and apob >= 130:
        factors.append(f"Elevated ApoB ({apob:.0f} mg/dL)")
    if ldl and ldl >= 190:
        factors.append(f"Severe hypercholesterolemia (LDL {ldl:.0f} mg/dL)")
    elif ldl and ldl >= 160:
        factors.append(f"High LDL cholesterol ({ldl:.0f} mg/dL)")
    if prem_ascvd:
        factors.append("Premature ASCVD in first-degree relatives")
    if fh_dm:
        factors.append("Family history of diabetes")
    if fh_htn:
        factors.append("Family history of hypertension")
    return factors


def get_aha_recommendations(aha_cat, aha_risk):
    if aha_cat == "Low":
        return {"statin": "Not recommended", "ldl_target": "<100 mg/dL (optional)", "non_hdl_target": "<130 mg/dL (optional)", "lifestyle": "Heart-healthy lifestyle, regular exercise, healthy diet", "monitoring": "Reassess in 4-6 years"}
    elif aha_cat == "Moderate":
        return {"statin": "Consider moderate-intensity statin", "ldl_target": "<100 mg/dL (preferred <70 mg/dL)", "non_hdl_target": "<130 mg/dL (preferred <100 mg/dL)", "lifestyle": "Aggressive lifestyle modification essential", "monitoring": "Reassess lipids in 3 months, then annually"}
    elif aha_cat == "High":
        return {"statin": "Moderate to high-intensity statin recommended", "ldl_target": "<70 mg/dL", "non_hdl_target": "<100 mg/dL", "lifestyle": "Intensive lifestyle intervention required", "monitoring": "Lipid panel at 4-12 weeks, optimize therapy"}
    else:
        return {"statin": "High-intensity statin ± ezetimibe recommended", "ldl_target": "<50 mg/dL", "non_hdl_target": "<80 mg/dL", "lifestyle": "Comprehensive risk factor management essential", "monitoring": "Frequent monitoring, consider PCSK9i if targets not met"}


def get_qrisk_recommendations(qrisk_cat, qrisk_value):
    if qrisk_cat == "Low":
        return {"statin": "Not indicated", "ldl_target": "<100 mg/dL", "non_hdl_target": "<130 mg/dL", "lifestyle": "Maintain healthy lifestyle, regular physical activity", "monitoring": "Reassess cardiovascular risk every 5 years"}
    elif qrisk_cat == "Moderate":
        return {"statin": "Discuss benefits and risks with patient", "ldl_target": "<100 mg/dL (consider <70 mg/dL)", "non_hdl_target": "<130 mg/dL (consider <100 mg/dL)", "lifestyle": "Optimize lifestyle factors first, then consider pharmacotherapy", "monitoring": "Annual risk assessment and lipid monitoring"}
    elif qrisk_cat == "High":
        return {"statin": "Atorvastatin 20mg or equivalent recommended", "ldl_target": "<70 mg/dL", "non_hdl_target": "<100 mg/dL", "lifestyle": "Intensive lifestyle modification alongside statin therapy", "monitoring": "Lipids at 3 months, then 6-12 monthly"}
    else:
        return {"statin": "Atorvastatin 80mg or rosuvastatin 20-40mg recommended", "ldl_target": "<50 mg/dL", "non_hdl_target": "<80 mg/dL", "lifestyle": "Multifactorial risk reduction strategy required", "monitoring": "Close monitoring, escalate therapy as needed"}


def get_lai_recommendations(lai_cat):
    if lai_cat == "Low":
        return {"statin": "Not recommended - lifestyle only", "ldl_target": "<100 mg/dL", "non_hdl_target": "<130 mg/dL", "apob_target": "<90 mg/dL", "lifestyle": "Heart-healthy Indian diet, regular exercise, avoid tobacco", "monitoring": "Reassess every 3-5 years"}
    elif lai_cat == "Moderate":
        return {"statin": "Moderate-intensity statin (consider for South Asians)", "ldl_target": "<100 mg/dL (optional <70 mg/dL)", "non_hdl_target": "<130 mg/dL (optional <100 mg/dL)", "apob_target": "<90 mg/dL", "lifestyle": "Aggressive lifestyle measures, weight management", "monitoring": "Annual lipid profile and cardiovascular risk assessment"}
    elif lai_cat == "High":
        return {"statin": "High-intensity statin therapy recommended", "ldl_target": "<70 mg/dL", "non_hdl_target": "<100 mg/dL", "apob_target": "<80 mg/dL", "lifestyle": "Comprehensive lifestyle intervention, manage all risk factors", "monitoring": "Lipids at 4 weeks, then every 3 months until stable"}
    else:
        return {"statin": "High-intensity statin + ezetimibe, consider PCSK9i", "ldl_target": "<50 mg/dL", "non_hdl_target": "<80 mg/dL", "apob_target": "<65 mg/dL", "lifestyle": "Intensive multi-factorial risk reduction essential", "monitoring": "Frequent monitoring, aggressive target achievement required"}


def generate_fallback_summary(aha_cat, qrisk_cat, lai_cat):
    levels = {"Low": 0, "Moderate": 1, "High": 2, "Very High": 3}
    scores = []
    if aha_cat:
        scores.append((levels.get(aha_cat, 0), aha_cat, "AHA PREVENT"))
    if qrisk_cat:
        scores.append((levels.get(qrisk_cat, 0), qrisk_cat, "QRISK3"))
    if lai_cat:
        scores.append((levels.get(lai_cat, 0), lai_cat, "LAI"))
    if not scores:
        return "Insufficient data for comprehensive risk assessment."
    max_risk = max(scores, key=lambda x: x[0])
    summary = f"""**Overall Risk Level:** {max_risk[1]} (driven primarily by {max_risk[2]})\n\n"""
    if max_risk[1] in ["High", "Very High"]:
        summary += """**Statin Therapy:** RECOMMENDED
- High-intensity statin (Atorvastatin 40-80mg or Rosuvastatin 20-40mg)
- Add ezetimibe 10mg if LDL-C targets not achieved
- Consider PCSK9 inhibitor for Very High risk if targets remain unmet

**Lipid Targets:**
- LDL-C: <70 mg/dL (Very High: <50 mg/dL)
- Non-HDL-C: <100 mg/dL (Very High: <80 mg/dL)
- ApoB: <80 mg/dL (Very High: <65 mg/dL)

**Lifestyle:** Heart-healthy diet · Physical activity ≥150 min/week · Weight management · Smoking cessation

**Monitoring:** Lipid panel at 4-6 weeks → every 3 months until targets achieved → 6-monthly
"""
    elif max_risk[1] == "Moderate":
        summary += """**Statin Therapy:** CONSIDER (shared decision-making)
- Moderate-intensity statin (Atorvastatin 10-20mg or Rosuvastatin 5-10mg)
- Especially recommended for South Asian ethnicity

**Lipid Targets:**
- LDL-C: <100 mg/dL (consider <70 mg/dL)
- Non-HDL-C: <130 mg/dL (consider <100 mg/dL)

**Lifestyle:** Aggressive lifestyle modification as first-line · Weight reduction if BMI ≥25

**Monitoring:** Reassess in 3-6 months · Annual lipid profile and risk assessment
"""
    else:
        summary += """**Statin Therapy:** NOT RECOMMENDED — continue lifestyle measures

**Targets:** LDL-C <100 mg/dL · Non-HDL-C <130 mg/dL

**Lifestyle:** Maintain healthy diet and regular physical activity

**Monitoring:** Periodic reassessment every 3-5 years
"""
    return summary


def calculate_qrisk3(age, sex, ethnicity, smoking, diabetes, height, weight, sbp, tc_hdl_ratio, antihtn, family_cvd, ckd, atrial_fib, rheumatoid_arthritis, migraine):
    required = [age, sex, tc_hdl_ratio, sbp]
    if None in required:
        return None
    if age < 25 or age > 84:
        return None
    bmi = bmi_calc(height, weight)
    if bmi is None:
        bmi = 25
    eth_code = {"Indian": 9, "South Asian": 9, "White": 1, "Black": 3, "Other": 1}.get(ethnicity, 1)
    smoke_code = {"Never": 0, "Former": 2, "Current": 4}.get(smoking, 0)
    is_female = sex == "Female"
    if is_female:
        survivor = 0.988876
        age_term = (age / 10) - 4.0
        smoking_param = smoke_code * 0.13
        diabetes_param = 0.86 if diabetes == "Yes" else 0
        bmi_param = 0.56 if bmi >= 30 else (0.23 if bmi >= 25 else (0.12 if bmi >= 20 else 0.0))
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
        bmi_param = 0.48 if bmi >= 30 else (0.20 if bmi >= 25 else (0.10 if bmi >= 20 else 0.0))
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
        coef_ln_age = 17.114; coef_ln_tc = 0.940; coef_ln_hdl = -18.920; coef_ln_age_hdl = 4.475
        coef_ln_treated_sbp = 29.291; coef_ln_age_treated_sbp = -6.432
        coef_ln_untreated_sbp = 27.820; coef_ln_age_untreated_sbp = -6.087
        coef_smoker = 0.691; coef_dm = 0.874; mean_sum = 86.61; baseline_survival = 0.9533
        individual_sum = (coef_ln_age * ln_age + coef_ln_tc * ln_tc + coef_ln_hdl * ln_hdl +
                          coef_ln_age_hdl * ln_age * ln_hdl + coef_ln_treated_sbp * ln_sbp_treated +
                          coef_ln_age_treated_sbp * ln_age * ln_sbp_treated +
                          coef_ln_untreated_sbp * ln_sbp_untreated +
                          coef_ln_age_untreated_sbp * ln_age * ln_sbp_untreated +
                          coef_smoker * smoker + coef_dm * dm)
    elif not is_black and is_female:
        coef_ln_age = -29.799; coef_ln_age_sq = 4.884; coef_ln_tc = 13.540; coef_ln_age_tc = -3.114
        coef_ln_hdl = -13.578; coef_ln_age_hdl = 3.149
        coef_ln_treated_sbp = 2.019; coef_ln_untreated_sbp = 1.957
        coef_smoker = 7.574; coef_ln_age_smoker = -1.665; coef_dm = 0.661
        mean_sum = -29.18; baseline_survival = 0.9665
        individual_sum = (coef_ln_age * ln_age + coef_ln_age_sq * ln_age * ln_age +
                          coef_ln_tc * ln_tc + coef_ln_age_tc * ln_age * ln_tc +
                          coef_ln_hdl * ln_hdl + coef_ln_age_hdl * ln_age * ln_hdl +
                          coef_ln_treated_sbp * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated +
                          coef_smoker * smoker + coef_ln_age_smoker * ln_age * smoker + coef_dm * dm)
    elif is_black and not is_female:
        coef_ln_age = 2.469; coef_ln_tc = 0.302; coef_ln_hdl = -0.307
        coef_ln_treated_sbp = 1.916; coef_ln_untreated_sbp = 1.809
        coef_smoker = 0.549; coef_dm = 0.645; mean_sum = 19.54; baseline_survival = 0.8954
        individual_sum = (coef_ln_age * ln_age + coef_ln_tc * ln_tc + coef_ln_hdl * ln_hdl +
                          coef_ln_treated_sbp * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated +
                          coef_smoker * smoker + coef_dm * dm)
    else:
        coef_ln_age = 12.344; coef_ln_tc = 11.853; coef_ln_age_tc = -2.664
        coef_ln_hdl = -7.990; coef_ln_age_hdl = 1.769
        coef_ln_treated_sbp = 1.797; coef_ln_untreated_sbp = 1.764
        coef_smoker = 7.837; coef_ln_age_smoker = -1.795; coef_dm = 0.658
        mean_sum = 61.18; baseline_survival = 0.9144
        individual_sum = (coef_ln_age * ln_age + coef_ln_tc * ln_tc +
                          coef_ln_age_tc * ln_age * ln_tc + coef_ln_hdl * ln_hdl +
                          coef_ln_age_hdl * ln_age * ln_hdl +
                          coef_ln_treated_sbp * ln_sbp_treated + coef_ln_untreated_sbp * ln_sbp_untreated +
                          coef_smoker * smoker + coef_ln_age_smoker * ln_age * smoker + coef_dm * dm)
    risk_10yr = (1 - math.pow(baseline_survival, math.exp(individual_sum - mean_sum))) * 100
    return round(min(risk_10yr, 100), 1)


# ==================== HEADER ====================

header_cols = st.columns([2, 1])

with header_cols[0]:
    st.markdown(
        '<div class="main-title">🫀 Cardiovascular Risk Assessment Tool</div>',
        unsafe_allow_html=True
    )

with header_cols[1]:
    ref1, ref2 = st.columns(2)
    with ref1:
        st.markdown(
            '<a href="https://professional.heart.org/en/guidelines-and-statements/prevent-calculator" target="_blank" class="cv-ref-pill">↗ AHA PREVENT</a>',
            unsafe_allow_html=True
        )
    with ref2:
        st.markdown(
            '<a href="https://qrisk.org/" target="_blank" class="cv-ref-pill">↗ QRISK3</a>',
            unsafe_allow_html=True
        )

controls = st.columns([3, 1, 1])

with controls[1]:
    st.markdown('<div class="cv-reset-btn">', unsafe_allow_html=True)
    if st.button("↺ Reset", key="btn_reset"):
        reset_all()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with controls[2]:
    st.markdown('<div class="cv-theme-btn">', unsafe_allow_html=True)
    st.button(
        f"{TOGGLE_ICON} {'Light Mode' if is_dark else 'Dark Mode'}",
        key="btn_theme",
        on_click=toggle_theme
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

# ==================== FAMILY HISTORY ====================
sep("Family History")
st.caption("Premature ASCVD: Male <55 yrs · Female <65 yrs in first-degree relatives")

if 'none_fh' not in st.session_state:
    st.session_state.none_fh = False

fh1, fh2 = st.columns(2)
with fh1:
    prem_ascvd = st.checkbox("Premature ASCVD (first-degree relatives)", disabled=st.session_state.none_fh, key="prem_ascvd")
    fh_dm = st.checkbox("Family Hx of Diabetes", disabled=st.session_state.none_fh, key="fh_dm")

with fh2:
    fh_htn = st.checkbox("Family Hx of Hypertension", disabled=st.session_state.none_fh, key="fh_htn")
    fh_fh = st.checkbox("Familial Hypercholesterolemia", disabled=st.session_state.none_fh, key="fh_fh")

none_fh_check = st.checkbox("None of the above", key="none_fh_check")
if none_fh_check != st.session_state.none_fh:
    st.session_state.none_fh = none_fh_check
    if none_fh_check:
        for k in ['prem_ascvd', 'fh_dm', 'fh_htn', 'fh_fh']:
            if k in st.session_state:
                st.session_state[k] = False
    st.rerun()


# ==================== MEDICATIONS ====================
sep("Current Medications")

if 'none_med' not in st.session_state:
    st.session_state.none_med = False

med1, med2 = st.columns(2)
with med1:
    on_statin = st.checkbox("Statin", disabled=st.session_state.none_med, key="on_statin")
    antihtn = st.checkbox("Antihypertensive", disabled=st.session_state.none_med, key="antihtn")

with med2:
    antidm = st.checkbox("Antidiabetic", disabled=st.session_state.none_med, key="antidm")
    antiplate = st.checkbox("Antiplatelet", disabled=st.session_state.none_med, key="antiplate")

none_med_check = st.checkbox("None of the above", key="none_med_check")
if none_med_check != st.session_state.none_med:
    st.session_state.none_med = none_med_check
    if none_med_check:
        for k in ['on_statin', 'antihtn', 'antidm', 'antiplate']:
            if k in st.session_state:
                st.session_state[k] = False
    st.rerun()


# ==================== CALCULATIONS ====================
qrisk = calculate_qrisk3(age_val, sex, eth, smoke, diabetes, height_val, weight_val, sbp, tc_hdl_ratio, antihtn, prem_ascvd, ckd, atrial_fib, rheumatoid_arthritis, migraine)
aha = calculate_aha_prevent(age_val, sex, eth, tc, hdl, sbp, antihtn, diabetes, smoke)
qrisk_cat = percent_category(qrisk)
aha_cat = percent_category(aha)

risk_enhancers = (smoke == "Current") or mets or fh_fh or (lpa is not None and lpa > 50) or (apob is not None and apob > 130)
if ascvd or ckd or (diabetes == "Yes" and duration is not None and duration >= 10):
    lai = "Very High"
elif diabetes == "Yes" or risk_enhancers:
    lai = "High"
elif prem_ascvd or fh_dm or fh_htn:
    lai = "Moderate"
else:
    lai = "Low"


# ==================== SCORE METRICS ====================
st.markdown('<div class="section-divider" style="margin-top:1.8rem;"></div>', unsafe_allow_html=True)
sep("Calculated 10-Year Risk Scores")

sc1, sc2, sc3 = st.columns(3)
with sc1:
    if qrisk is not None:
        sc1.metric("QRISK3", f"{qrisk}%", help="10-year CVD risk — requires age 25-84")
    else:
        st.info("QRISK3: Requires age 25–84 + complete inputs")

with sc2:
    if aha is not None:
        sc2.metric("AHA PREVENT", f"{aha}%", help="10-year ASCVD risk — requires age 40-79")
    else:
        st.info("AHA PREVENT: Requires age 40–79 + complete inputs")

with sc3:
    sc3.metric("LAI 2023 Category", lai)


# ==================== RISK STRATIFICATION PANEL ====================
sep("Risk Stratification")

cols = st.columns(3)

with cols[0]:
    if aha_cat:
        cat_class = aha_cat.lower().replace(" ", "")
        st.markdown(
            f'<div class="risk-card risk-{cat_class}">'
            f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:0.3rem;">AHA PREVENT</div>'
            f'<div style="font-size:1.7rem;font-weight:800;color:{TEXT_PRIMARY};line-height:1.1;">{aha_cat}</div>'
            f'<div style="font-size:1rem;font-weight:600;color:{TEXT_SECONDARY};margin-top:0.2rem;">{aha}% · 10-yr ASCVD</div>'
            f'</div>', unsafe_allow_html=True
        )
        if aha_cat != "Low":
            factors = get_contributing_factors_aha(age_val, sex, tc, hdl, sbp, antihtn, diabetes, smoke)
            if factors:
                st.markdown(
                    f'<div class="contributing-factors"><div class="factor-title">Key Drivers</div>' +
                    "".join(f'<div class="factor-item">{f}</div>' for f in factors[:5]) +
                    '</div>', unsafe_allow_html=True
                )
    else:
        st.markdown(
            f'<div class="risk-card risk-unavailable">'
            f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:0.3rem;">AHA PREVENT</div>'
            f'<div style="font-size:1rem;color:{TEXT_MUTED};">Not calculable</div>'
            f'<div style="font-size:0.78rem;color:{TEXT_MUTED};margin-top:0.2rem;">Requires age 40–79 + lipids + BP</div>'
            f'</div>', unsafe_allow_html=True
        )

with cols[1]:
    if qrisk_cat:
        cat_class = qrisk_cat.lower().replace(" ", "")
        st.markdown(
            f'<div class="risk-card risk-{cat_class}">'
            f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:0.3rem;">QRISK3</div>'
            f'<div style="font-size:1.7rem;font-weight:800;color:{TEXT_PRIMARY};line-height:1.1;">{qrisk_cat}</div>'
            f'<div style="font-size:1rem;font-weight:600;color:{TEXT_SECONDARY};margin-top:0.2rem;">{qrisk}% · 10-yr CVD</div>'
            f'</div>', unsafe_allow_html=True
        )
        if qrisk_cat != "Low":
            factors = get_contributing_factors_qrisk(age_val, sex, smoke, diabetes, bmi, sbp, tc_hdl_ratio, prem_ascvd, ckd, atrial_fib, rheumatoid_arthritis, eth)
            if factors:
                st.markdown(
                    f'<div class="contributing-factors"><div class="factor-title">Key Drivers</div>' +
                    "".join(f'<div class="factor-item">{f}</div>' for f in factors[:5]) +
                    '</div>', unsafe_allow_html=True
                )
    else:
        st.markdown(
            f'<div class="risk-card risk-unavailable">'
            f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:0.3rem;">QRISK3</div>'
            f'<div style="font-size:1rem;color:{TEXT_MUTED};">Not calculable</div>'
            f'<div style="font-size:0.78rem;color:{TEXT_MUTED};margin-top:0.2rem;">Requires age 25–84 + TC/HDL ratio + BP</div>'
            f'</div>', unsafe_allow_html=True
        )

with cols[2]:
    cat_class = lai.lower().replace(" ", "")
    st.markdown(
        f'<div class="risk-card risk-{cat_class}">'
        f'<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:0.3rem;">LAI 2023</div>'
        f'<div style="font-size:1.7rem;font-weight:800;color:{TEXT_PRIMARY};line-height:1.1;">{lai}</div>'
        f'<div style="font-size:0.82rem;color:{TEXT_SECONDARY};margin-top:0.2rem;font-style:italic;">Lipid Association of India</div>'
        f'</div>', unsafe_allow_html=True
    )
    if lai != "Low":
        factors = get_contributing_factors_lai(ascvd, ckd, diabetes, duration, smoke, mets, fh_fh, lpa, apob, prem_ascvd, fh_dm, fh_htn, ldl)
        if factors:
            st.markdown(
                f'<div class="contributing-factors"><div class="factor-title">Key Drivers</div>' +
                "".join(f'<div class="factor-item">{f}</div>' for f in factors[:5]) +
                '</div>', unsafe_allow_html=True
            )


# ==================== TREATMENT RECOMMENDATIONS ====================
sep("Treatment Recommendations by Guideline")

tab1, tab2, tab3 = st.tabs(["AHA PREVENT", "QRISK3", "LAI 2023"])

with tab1:
    if aha_cat:
        recs = get_aha_recommendations(aha_cat, aha)
        st.markdown(f"**{aha_cat} Risk** — AHA PREVENT")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Statin Therapy:** {recs['statin']}")
            st.markdown(f"**LDL-C Target:** {recs['ldl_target']}")
            st.markdown(f"**Non-HDL-C Target:** {recs['non_hdl_target']}")
        with c2:
            st.markdown(f"**Lifestyle:** {recs['lifestyle']}")
            st.markdown(f"**Monitoring:** {recs['monitoring']}")
    else:
        st.info("AHA PREVENT score not calculable with current data.")

with tab2:
    if qrisk_cat:
        recs = get_qrisk_recommendations(qrisk_cat, qrisk)
        st.markdown(f"**{qrisk_cat} Risk** — QRISK3")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Statin Therapy:** {recs['statin']}")
            st.markdown(f"**LDL-C Target:** {recs['ldl_target']}")
            st.markdown(f"**Non-HDL-C Target:** {recs['non_hdl_target']}")
        with c2:
            st.markdown(f"**Lifestyle:** {recs['lifestyle']}")
            st.markdown(f"**Monitoring:** {recs['monitoring']}")
    else:
        st.info("QRISK3 score not calculable with current data.")

with tab3:
    recs = get_lai_recommendations(lai)
    st.markdown(f"**{lai} Risk** — LAI 2023")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Statin Therapy:** {recs['statin']}")
        st.markdown(f"**LDL-C Target:** {recs['ldl_target']}")
        st.markdown(f"**Non-HDL-C Target:** {recs['non_hdl_target']}")
        st.markdown(f"**ApoB Target:** {recs['apob_target']}")
    with c2:
        st.markdown(f"**Lifestyle:** {recs['lifestyle']}")
        st.markdown(f"**Monitoring:** {recs['monitoring']}")


# ==================== UNIFIED RECOMMENDATION ====================
sep("Unified Clinical Recommendation")

unified_summary = generate_fallback_summary(aha_cat, qrisk_cat, lai)
st.markdown(unified_summary)

st.info("This recommendation synthesizes AHA PREVENT, QRISK3, and LAI 2023 guidelines. All decisions should involve shared decision-making with the patient.")

st.markdown('<div class="section-divider" style="margin-top:2rem;"></div>', unsafe_allow_html=True)

# ==================== REFERENCE LINKS ====================
st.markdown("""
<div class="premium-link-container">
    <a href="https://professional.heart.org/en/guidelines-and-statements/prevent-calculator" target="_blank" class="premium-link">
        <div class="premium-link-title">AHA PREVENT</div>
        <div class="premium-link-subtitle">American Heart Association</div>
    </a>
    <a href="https://qrisk.org/" target="_blank" class="premium-link qrisk">
        <div class="premium-link-title">QRISK3</div>
        <div class="premium-link-subtitle">UK CVD Risk Calculator</div>
    </a>
    <a href="https://www.lipidjournal.com/article/S1933-2874(24)00006-0/fulltext" target="_blank" class="premium-link lai">
        <div class="premium-link-title">LAI 2023</div>
        <div class="premium-link-subtitle">Lipid Association of India</div>
    </a>
</div>
""", unsafe_allow_html=True)

st.caption("Clinical decision support tool — AHA · QRISK3 · LAI 2023 Guidelines. All treatment decisions require clinical judgment and shared decision-making.")
