import streamlit as st
import math
import json

st.set_page_config(
    layout="wide",
    page_title="🫀 Cardiovascular Risk Assessment Tool",
    initial_sidebar_state="collapsed"
)

# ========== THEME MANAGEMENT ==========
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

is_dark = st.session_state.theme == "dark"

# ========== THEME VARIABLES ==========
if is_dark:
    BG_PAGE        = "#0f1117"
    BG_SECONDARY   = "#1a1d27"
    BG_INPUT       = "#252836"
    BG_CARD        = "#1e2130"
    TEXT_PRIMARY   = "#e8eaf0"
    TEXT_SECONDARY = "#9aa0b8"
    TEXT_MUTED     = "#6b7280"
    BORDER_COLOR   = "#2e3347"
    ACCENT         = "#4c9ef8"
    ACCENT_DARK    = "#3a82d6"
    HEADING_COLOR  = "#cbd5f5"
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
    # Risk card dark variants
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
    TOGGLE_ICON       = "☀️"
    TOGGLE_LABEL      = "Light Mode"
    SELECTBOX_COLOR   = "#e8eaf0"
    INPUT_COLOR       = "#e8eaf0"
    CAPTION_COLOR     = "#9aa0b8"
    TAB_BG            = "#1a1d27"
    TAB_ACTIVE_BG     = "#252836"
    TAB_COLOR         = "#9aa0b8"
    TAB_ACTIVE_COLOR  = "#4c9ef8"
    TAB_ACTIVE_BORDER = "#4c9ef8"
else:
    BG_PAGE        = "#f5f7fa"
    BG_SECONDARY   = "#ffffff"
    BG_INPUT       = "#ffffff"
    BG_CARD        = "#ffffff"
    TEXT_PRIMARY   = "#2d3748"
    TEXT_SECONDARY = "#4a5568"
    TEXT_MUTED     = "#718096"
    BORDER_COLOR   = "#e2e8f0"
    ACCENT         = "#4299e1"
    ACCENT_DARK    = "#2c5282"
    HEADING_COLOR  = "#1a365d"
    H2_LEFT_BAR    = "#4299e1"
    H2_BG          = "rgba(66, 153, 225, 0.1)"
    DIVIDER        = "#e2e8f0"
    METRIC_BG      = "#ffffff"
    METRIC_VAL     = "#1a365d"
    BTN_BG         = "#2c5282"
    BTN_HOVER      = "#1a365d"
    INFO_BG        = "#e6f3ff"
    INFO_BORDER    = "#4299e1"
    WARN_BG        = "#fff3cd"
    WARN_BORDER    = "#ffc107"
    # Risk card light variants
    RISK_LOW_BG       = "linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)"
    RISK_LOW_BORDER   = "#28a745"
    RISK_MOD_BG       = "linear-gradient(135deg, #fff3cd 0%, #ffe8a1 100%)"
    RISK_MOD_BORDER   = "#ffc107"
    RISK_HIGH_BG      = "linear-gradient(135deg, #ffd6a5 0%, #ffcc80 100%)"
    RISK_HIGH_BORDER  = "#ff9800"
    RISK_VH_BG        = "linear-gradient(135deg, #f8d7da 0%, #f1b0b7 100%)"
    RISK_VH_BORDER    = "#dc3545"
    RISK_NA_BG        = "linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%)"
    RISK_NA_BORDER    = "#6c757d"
    CF_BG             = "rgba(255,255,255,0.8)"
    CF_BORDER         = "rgba(0,0,0,0.08)"
    CF_TITLE          = "#2d3748"
    CF_ITEM           = "#4a5568"
    CF_BULLET         = "#4299e1"
    TOGGLE_ICON       = "🌙"
    TOGGLE_LABEL      = "Dark Mode"
    SELECTBOX_COLOR   = "#2d3748"
    INPUT_COLOR       = "#2d3748"
    CAPTION_COLOR     = "#4a5568"
    TAB_BG            = "#f7fafc"
    TAB_ACTIVE_BG     = "#ffffff"
    TAB_COLOR         = "#4a5568"
    TAB_ACTIVE_COLOR  = "#2c5282"
    TAB_ACTIVE_BORDER = "#4299e1"

# ========== INJECT CSS ==========
st.markdown(f"""
<style>
    /* ---- Toolbar / menu hiding ---- */
    button[kind="header"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    #MainMenu {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}

    /* ---- Global page ---- */
    html, body, .stApp, .main, [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"] {{
        background-color: {BG_PAGE} !important;
        color: {TEXT_PRIMARY} !important;
    }}

    /* ---- Block container ---- */
    .block-container {{
        background-color: {BG_PAGE} !important;
        padding-top: 2rem !important;
    }}

    /* ---- Universal text reset ---- */
    .stApp *, p, span, div, label, li {{
        color: {TEXT_PRIMARY} !important;
    }}

    /* ---- Headings ---- */
    h1 {{
        color: {HEADING_COLOR} !important;
        font-weight: 700 !important;
        border-bottom: 3px solid {ACCENT} !important;
        padding-bottom: 0.8rem !important;
        margin-bottom: 1.5rem !important;
        margin-top: 0 !important;
    }}
    h2 {{
        color: {TEXT_PRIMARY} !important;
        font-weight: 600 !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1.5rem !important;
        border-left: 5px solid {H2_LEFT_BAR} !important;
        padding-left: 1.2rem !important;
        padding-top: 0.6rem !important;
        padding-bottom: 0.6rem !important;
        background: linear-gradient(90deg, {H2_BG} 0%, transparent 100%) !important;
    }}
    h3 {{
        color: {TEXT_PRIMARY} !important;
        font-weight: 600 !important;
    }}

    /* ---- Number inputs ---- */
    .stNumberInput input,
    input[type="number"],
    input[type="text"] {{
        background-color: {BG_INPUT} !important;
        color: {INPUT_COLOR} !important;
        border: 2px solid {BORDER_COLOR} !important;
        border-radius: 6px !important;
        caret-color: {INPUT_COLOR} !important;
    }}
    .stNumberInput input:focus {{
        border-color: {ACCENT} !important;
        box-shadow: 0 0 0 3px {ACCENT}33 !important;
        outline: none !important;
    }}
    /* Stepper buttons */
    .stNumberInput [data-testid="stNumberInputStepUp"],
    .stNumberInput [data-testid="stNumberInputStepDown"],
    .stNumberInput button {{
        background-color: {BG_INPUT} !important;
        color: {INPUT_COLOR} !important;
        border-color: {BORDER_COLOR} !important;
    }}
    .stNumberInput [data-testid="stNumberInputStepUp"]:hover,
    .stNumberInput [data-testid="stNumberInputStepDown"]:hover,
    .stNumberInput button:hover {{
        background-color: {BORDER_COLOR} !important;
    }}

    /* ---- Selectbox / Dropdown ---- */
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox [data-baseweb="select"] > div > div,
    [data-baseweb="select"] [data-testid="stMarkdownContainer"] {{
        background-color: {BG_INPUT} !important;
        color: {SELECTBOX_COLOR} !important;
        border-color: {BORDER_COLOR} !important;
    }}
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div {{
        color: {SELECTBOX_COLOR} !important;
        background-color: transparent !important;
    }}
    /* Dropdown popup list */
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"],
    [data-baseweb="list"] {{
        background-color: {BG_INPUT} !important;
        border-color: {BORDER_COLOR} !important;
    }}
    [role="option"],
    [data-baseweb="option"] {{
        background-color: {BG_INPUT} !important;
        color: {SELECTBOX_COLOR} !important;
    }}
    [role="option"]:hover,
    [data-baseweb="option"]:hover {{
        background-color: {BORDER_COLOR} !important;
    }}

    /* ---- Radio buttons ---- */
    .stRadio label, .stRadio div {{
        color: {TEXT_PRIMARY} !important;
    }}
    .stRadio [data-testid="stMarkdownContainer"] p {{
        color: {TEXT_PRIMARY} !important;
    }}

    /* ---- Checkboxes ---- */
    .stCheckbox label, .stCheckbox span, .stCheckbox p {{
        color: {TEXT_PRIMARY} !important;
        font-weight: 500 !important;
    }}
    .stCheckbox {{
        margin-bottom: 0.4rem !important;
    }}

    /* ---- Labels for all widgets ---- */
    .stSelectbox label,
    .stNumberInput label,
    .stTextInput label,
    .stRadio label,
    [data-testid="stWidgetLabel"] {{
        color: {TEXT_PRIMARY} !important;
        font-weight: 500 !important;
    }}

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {BG_SECONDARY} !important;
        gap: 0.5rem !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: {TAB_COLOR} !important;
        background-color: {TAB_BG} !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {TAB_ACTIVE_COLOR} !important;
        background-color: {TAB_ACTIVE_BG} !important;
        border-bottom: 3px solid {TAB_ACTIVE_BORDER} !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{
        background-color: {BG_SECONDARY} !important;
        padding: 1.5rem !important;
        border-radius: 0 0 8px 8px !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-top: none !important;
    }}

    /* ---- Metric widget ---- */
    [data-testid="stMetric"] {{
        background-color: {METRIC_BG} !important;
        padding: 1.2rem !important;
        border-radius: 8px !important;
        border: 1px solid {BORDER_COLOR} !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {TEXT_SECONDARY} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {METRIC_VAL} !important;
        font-weight: 700 !important;
    }}

    /* ---- Alert boxes (info, warning, success) ---- */
    [data-testid="stAlert"],
    .stAlert {{
        border-radius: 6px !important;
    }}
    div[data-testid="stAlert"][kind="info"],
    .element-container div[kind="info"] {{
        background-color: {INFO_BG} !important;
        border-left: 5px solid {INFO_BORDER} !important;
    }}
    div[data-testid="stAlert"][kind="warning"],
    .element-container div[kind="warning"] {{
        background-color: {WARN_BG} !important;
        border-left: 5px solid {WARN_BORDER} !important;
    }}

    /* ---- Buttons ---- */
    .stButton > button {{
        background-color: {BTN_BG} !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 1.8rem !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
    }}
    .stButton > button:hover {{
        background-color: {BTN_HOVER} !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    }}

    /* ---- Theme toggle button (special override) ---- */
    .theme-toggle-btn .stButton > button {{
        background-color: transparent !important;
        color: {TEXT_PRIMARY} !important;
        border: 2px solid {BORDER_COLOR} !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1rem !important;
        box-shadow: none !important;
    }}
    .theme-toggle-btn .stButton > button:hover {{
        background-color: {BORDER_COLOR} !important;
        transform: none !important;
    }}

    /* ---- Markdown ---- */
    .stMarkdown, .stMarkdown p, .stMarkdown span,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{
        color: {TEXT_PRIMARY} !important;
    }}

    /* ---- Caption ---- */
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {CAPTION_COLOR} !important;
    }}

    /* ---- HR divider ---- */
    hr {{
        border: none !important;
        border-top: 2px solid {DIVIDER} !important;
        margin: 2.5rem 0 !important;
    }}

    /* ---- Risk cards (custom HTML) ---- */
    .risk-card {{
        border-radius: 10px !important;
        padding: 1.5rem !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        border: 1px solid {BORDER_COLOR} !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }}
    .risk-card:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }}
    .risk-card h1, .risk-card h3, .risk-card p {{
        color: {TEXT_PRIMARY} !important;
    }}
    .risk-low  {{ background: {RISK_LOW_BG}  !important; border-left: 5px solid {RISK_LOW_BORDER}  !important; }}
    .risk-moderate {{ background: {RISK_MOD_BG}  !important; border-left: 5px solid {RISK_MOD_BORDER}  !important; }}
    .risk-high {{ background: {RISK_HIGH_BG} !important; border-left: 5px solid {RISK_HIGH_BORDER} !important; }}
    .risk-veryhigh {{ background: {RISK_VH_BG} !important; border-left: 5px solid {RISK_VH_BORDER} !important; }}
    .risk-unavailable {{ background: {RISK_NA_BG} !important; border-left: 5px solid {RISK_NA_BORDER} !important; }}

    /* ---- Contributing factors block ---- */
    .contributing-factors {{
        background-color: {CF_BG} !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-top: 1.2rem !important;
        font-size: 0.9rem !important;
        border: 1px solid {CF_BORDER} !important;
    }}
    .factor-title {{
        font-weight: 600 !important;
        color: {CF_TITLE} !important;
        margin-bottom: 0.6rem !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }}
    .factor-item {{
        color: {CF_ITEM} !important;
        padding: 0.3rem 0 0.3rem 1.2rem !important;
        position: relative !important;
        line-height: 1.5 !important;
    }}
    .factor-item:before {{
        content: "▪" !important;
        position: absolute !important;
        left: 0 !important;
        font-weight: bold !important;
        color: {CF_BULLET} !important;
    }}

    /* ---- Premium link buttons ---- */
    .premium-link-container {{
        display: flex !important;
        gap: 1rem !important;
        margin: 1.5rem 0 !important;
        flex-wrap: wrap !important;
    }}
    .premium-link {{
        flex: 1 !important;
        min-width: 220px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 1.2rem 1.5rem !important;
        border-radius: 12px !important;
        text-decoration: none !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
        text-align: center !important;
    }}
    .premium-link:hover {{
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 25px rgba(102,126,234,0.6) !important;
    }}
    .premium-link-title {{
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.3rem !important;
        color: white !important;
    }}
    .premium-link-subtitle {{
        font-size: 0.85rem !important;
        opacity: 0.9 !important;
        color: white !important;
    }}
    .premium-link.qrisk  {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important; box-shadow: 0 4px 15px rgba(240,147,251,0.4) !important; }}
    .premium-link.qrisk:hover {{ box-shadow: 0 8px 25px rgba(240,147,251,0.6) !important; }}
    .premium-link.lai    {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important; box-shadow: 0 4px 15px rgba(79,172,254,0.4) !important; }}
    .premium-link.lai:hover {{ box-shadow: 0 8px 25px rgba(79,172,254,0.6) !important; }}

    /* ---- Section divider ---- */
    .section-divider {{
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, {ACCENT} 0%, transparent 100%) !important;
        margin: 3rem 0 !important;
    }}

    /* ---- Disabled widget text ---- */
    .stCheckbox [disabled] + span,
    .stCheckbox input:disabled + span {{
        color: {TEXT_MUTED} !important;
        opacity: 0.7 !important;
    }}

    /* ---- Spinner text ---- */
    .stSpinner > div > div {{
        border-top-color: {ACCENT} !important;
    }}

    /* ---- Recommendation box ---- */
    .recommendation-box {{
        background-color: {BG_SECONDARY} !important;
        border-radius: 8px !important;
        padding: 1.5rem !important;
        margin: 1rem 0 !important;
        border-left: 4px solid {ACCENT} !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
    }}

    /* ---- iOS Safari fix: prevent font scaling ---- */
    @media screen and (max-width: 768px) {{
        input, select, textarea {{
            font-size: 16px !important;
        }}
    }}

    /* ---- Force input/select colors on all platforms ---- */
    input, select, textarea, [contenteditable] {{
        background-color: {BG_INPUT} !important;
        color: {INPUT_COLOR} !important;
    }}

    /* ---- Streamlit's internal iframe/component wrappers ---- */
    iframe {{
        background-color: {BG_PAGE} !important;
    }}

    /* ---- Scrollbar theming (non-Safari) ---- */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: {BG_PAGE}; }}
    ::-webkit-scrollbar-thumb {{ background: {BORDER_COLOR}; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {ACCENT}; }}
</style>
""", unsafe_allow_html=True)


# ========== HELPER FUNCTIONS ==========

def na_number(container, label, default=None, minv=0.0, maxv=500.0, step=1.0, key=None):
    col1, col2 = container.columns([5, 1])
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
    summary = f"""**Unified Clinical Recommendation:**

**Overall Risk Level:** {max_risk[1]} (driven primarily by {max_risk[2]})

"""
    if max_risk[1] in ["High", "Very High"]:
        summary += """**Statin Therapy:** RECOMMENDED
- High-intensity statin (Atorvastatin 40-80mg or Rosuvastatin 20-40mg)
- Add ezetimibe 10mg if LDL-C targets not achieved
- Consider PCSK9 inhibitor for Very High risk if targets remain unmet

**Lipid Targets:**
- LDL-C: <70 mg/dL (Very High: <50 mg/dL)
- Non-HDL-C: <100 mg/dL (Very High: <80 mg/dL)
- ApoB: <80 mg/dL (Very High: <65 mg/dL)

**Lifestyle Interventions:**
- Heart-healthy Indian diet (reduce saturated fats, increase fiber)
- Regular physical activity (150 min/week moderate intensity)
- Weight management if overweight
- Smoking cessation if applicable

**Monitoring:**
- Lipid panel at 4-6 weeks after initiation
- Monitor liver enzymes and CK if symptomatic
- Reassess every 3 months until targets achieved, then 6-monthly
"""
    elif max_risk[1] == "Moderate":
        summary += """**Statin Therapy:** CONSIDER (Shared decision-making)
- Moderate-intensity statin (Atorvastatin 10-20mg or Rosuvastatin 5-10mg)
- Especially recommended for South Asian ethnicity

**Lipid Targets:**
- LDL-C: <100 mg/dL (consider <70 mg/dL)
- Non-HDL-C: <130 mg/dL (consider <100 mg/dL)

**Lifestyle Interventions:**
- Aggressive lifestyle modification as first-line
- Heart-healthy diet and regular exercise
- Weight reduction if BMI ≥25 kg/m²

**Monitoring:**
- Reassess in 3-6 months with lifestyle changes
- Annual lipid profile and risk assessment
"""
    else:
        summary += """**Statin Therapy:** NOT RECOMMENDED
- Continue heart-healthy lifestyle

**Targets:**
- Maintain LDL-C <100 mg/dL
- Non-HDL-C <130 mg/dL

**Lifestyle Interventions:**
- Maintain healthy diet and regular physical activity
- Periodic reassessment every 3-5 years
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


# ========== APP HEADER ==========

# Theme toggle in top-right
header_col1, header_col2 = st.columns([6, 1])
with header_col1:
    st.title("🫀 Cardiovascular Risk Assessment Tool")
    st.markdown("*Evidence-based risk stratification for clinical decision support*")
with header_col2:
    st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True)
    st.button(f"{TOGGLE_ICON} {TOGGLE_LABEL}", on_click=toggle_theme, key="theme_btn")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")

# ========== DEMOGRAPHICS ==========
st.header("Demographics")
st.markdown("")

age = na_number(st.container(), "Age (years)", minv=0, maxv=100, key="age")
st.markdown("")

colA, colB, colC = st.columns(3)
sex = colA.selectbox("Sex", ["Male", "Female"])
eth = colB.selectbox("Ethnicity", ["Indian", "South Asian", "White", "Black", "Other"])

st.markdown("")

height = na_number(colA, "Height (cm)", minv=100, maxv=220, key="h")
weight = na_number(colB, "Weight (kg)", minv=30, maxv=200, key="w")
bmi = bmi_calc(height, weight)
colC.metric("BMI (kg/m²)", f"{bmi:.1f}" if bmi is not None else "NA")

# ========== VITALS ==========
st.header("Vital Signs")
st.markdown("")

col1, col2 = st.columns(2)
sbp = na_number(col1, "Systolic BP (mmHg)", minv=70, maxv=240, key="sbp")
dbp = na_number(col2, "Diastolic BP (mmHg)", minv=40, maxv=140, key="dbp")

# ========== LIPIDS ==========
st.header("Lipid Profile")
st.markdown("")

r1c1, r1c2 = st.columns(2)
tc = na_number(r1c1, "Total Cholesterol (mg/dL)", minv=0, maxv=400, key="tc")
ldl = na_number(r1c2, "LDL Cholesterol (mg/dL)", minv=0, maxv=300, key="ldl")

st.markdown("")

r2c1, r2c2 = st.columns(2)
hdl = na_number(r2c1, "HDL Cholesterol (mg/dL)", minv=0, maxv=120, key="hdl")
tg = na_number(r2c2, "Triglycerides (mg/dL)", minv=0, maxv=600, key="tg")

st.markdown("")
nhdl = non_hdl(tc, hdl)
st.metric("Non-HDL Cholesterol (mg/dL)", f"{nhdl:.1f}" if nhdl is not None else "NA")

st.markdown("")
st.markdown("**Advanced Lipid Markers**")
st.markdown("")

r3c1, r3c2 = st.columns(2)
apob = na_number(r3c1, "Apolipoprotein B (mg/dL)", minv=0, maxv=200, key="apob")
apoa1 = na_number(r3c2, "Apolipoprotein A1 (mg/dL)", minv=0, maxv=250, key="apoa1")

st.markdown("")
apo_ratio = ratio(apob, apoa1)
st.metric("ApoB/ApoA1 Ratio", f"{apo_ratio:.2f}" if apo_ratio is not None else "NA")

st.markdown("")
lpa = na_number(st.container(), "Lipoprotein(a) (mg/dL)", minv=0, maxv=300, key="lpa")

# ========== DIABETES ==========
st.header("Diabetes Status")
st.markdown("")

diabetes = st.radio("Diabetes", ["No", "Yes"])
st.markdown("")

if diabetes == "Yes":
    duration = na_number(st.container(), "Diabetes Duration (years)", minv=0, maxv=50, key="dm_dur")
    st.markdown("")
    treatment = st.radio("Current Treatment", ["Oral", "Insulin"])
else:
    duration = None
    treatment = None

# ========== SMOKING ==========
st.header("Smoking History")
st.markdown("")

smoke = st.selectbox("Smoking Status", ["Never", "Former", "Current"])

# ========== MEDICAL HISTORY ==========
st.header("Medical History")
st.markdown("")

if 'none_hist' not in st.session_state:
    st.session_state.none_hist = False

col1, col2, col3 = st.columns(3)

with col1:
    mi = st.checkbox("Myocardial Infarction", disabled=st.session_state.none_hist, key="mi")
    stroke = st.checkbox("Stroke/TIA", disabled=st.session_state.none_hist, key="stroke")
    pad = st.checkbox("Peripheral Artery Disease", disabled=st.session_state.none_hist, key="pad")
    revasc = st.checkbox("Revascularization", disabled=st.session_state.none_hist, key="revasc")

with col2:
    ckd = st.checkbox("Chronic Kidney Disease", disabled=st.session_state.none_hist, key="ckd")
    hf = st.checkbox("Heart Failure", disabled=st.session_state.none_hist, key="hf")
    nafld = st.checkbox("NAFLD", disabled=st.session_state.none_hist, key="nafld")
    mets = st.checkbox("Metabolic Syndrome", disabled=st.session_state.none_hist, key="mets")

with col3:
    atrial_fib = st.checkbox("Atrial Fibrillation", disabled=st.session_state.none_hist, key="afib")
    rheumatoid_arthritis = st.checkbox("Rheumatoid Arthritis", disabled=st.session_state.none_hist, key="ra")
    migraine = st.checkbox("Migraine", disabled=st.session_state.none_hist, key="migraine")

st.markdown("")
none_hist_check = st.checkbox("None of the above", key="none_hist_check")

if none_hist_check != st.session_state.none_hist:
    st.session_state.none_hist = none_hist_check
    if none_hist_check:
        for key in ['mi', 'stroke', 'pad', 'revasc', 'ckd', 'hf', 'nafld', 'mets', 'afib', 'ra', 'migraine']:
            if key in st.session_state:
                st.session_state[key] = False
    st.rerun()

ascvd = mi or stroke or pad or revasc

# ========== FAMILY HISTORY ==========
st.header("Family History")
st.caption("Premature ASCVD = Male <55, Female <65 in first-degree relatives")
st.markdown("")

if 'none_fh' not in st.session_state:
    st.session_state.none_fh = False

col1, col2 = st.columns(2)

with col1:
    prem_ascvd = st.checkbox("Premature ASCVD in first-degree relatives", disabled=st.session_state.none_fh, key="prem_ascvd")
    fh_dm = st.checkbox("Family History of Diabetes", disabled=st.session_state.none_fh, key="fh_dm")

with col2:
    fh_htn = st.checkbox("Family History of Hypertension", disabled=st.session_state.none_fh, key="fh_htn")
    fh_fh = st.checkbox("Familial Hypercholesterolemia", disabled=st.session_state.none_fh, key="fh_fh")

st.markdown("")
none_fh_check = st.checkbox("None of the above", key="none_fh_check")

if none_fh_check != st.session_state.none_fh:
    st.session_state.none_fh = none_fh_check
    if none_fh_check:
        for key in ['prem_ascvd', 'fh_dm', 'fh_htn', 'fh_fh']:
            if key in st.session_state:
                st.session_state[key] = False
    st.rerun()

# ========== MEDICATIONS ==========
st.header("Current Medications")
st.markdown("")

if 'none_med' not in st.session_state:
    st.session_state.none_med = False

col1, col2 = st.columns(2)

with col1:
    on_statin = st.checkbox("Statin", disabled=st.session_state.none_med, key="on_statin")
    antihtn = st.checkbox("Antihypertensive", disabled=st.session_state.none_med, key="antihtn")

with col2:
    antidm = st.checkbox("Antidiabetic", disabled=st.session_state.none_med, key="antidm")
    antiplate = st.checkbox("Antiplatelet", disabled=st.session_state.none_med, key="antiplate")

st.markdown("")
none_med_check = st.checkbox("None of the above", key="none_med_check")

if none_med_check != st.session_state.none_med:
    st.session_state.none_med = none_med_check
    if none_med_check:
        for key in ['on_statin', 'antihtn', 'antidm', 'antiplate']:
            if key in st.session_state:
                st.session_state[key] = False
    st.rerun()

# ========== CALCULATIONS ==========
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.header("📊 Calculated Risk Scores")
st.markdown("")

tc_hdl_ratio = ratio(tc, hdl)
qrisk = calculate_qrisk3(age, sex, eth, smoke, diabetes, height, weight, sbp, tc_hdl_ratio, antihtn, prem_ascvd, ckd, atrial_fib, rheumatoid_arthritis, migraine)
aha = calculate_aha_prevent(age, sex, eth, tc, hdl, sbp, antihtn, diabetes, smoke)

col1, col2 = st.columns(2)
with col1:
    if qrisk is not None:
        st.metric("QRISK3 (10-year CVD risk)", f"{qrisk}%")
    else:
        st.info("QRISK3: Not calculable — requires age 25-84 and complete inputs")

with col2:
    if aha is not None:
        st.metric("AHA PREVENT (10-year ASCVD risk)", f"{aha}%")
    else:
        st.info("AHA PREVENT: Not calculable — requires age 40-79 and complete inputs")

qrisk_cat = percent_category(qrisk)
aha_cat = percent_category(aha)

st.markdown("")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

st.subheader("🔗 Official Guidelines & Calculators")
st.markdown("")

st.markdown("""
<div class="premium-link-container">
    <a href="https://professional.heart.org/en/guidelines-and-statements/prevent-calculator" target="_blank" class="premium-link">
        <div class="premium-link-title">AHA PREVENT</div>
        <div class="premium-link-subtitle">American Heart Association Calculator</div>
    </a>
    <a href="https://qrisk.org/" target="_blank" class="premium-link qrisk">
        <div class="premium-link-title">QRISK3</div>
        <div class="premium-link-subtitle">UK Cardiovascular Risk Calculator</div>
    </a>
    <a href="https://www.lipidjournal.com/article/S1933-2874(24)00006-0/fulltext" target="_blank" class="premium-link lai">
        <div class="premium-link-title">LAI 2023</div>
        <div class="premium-link-subtitle">Lipid Association of India Guidelines</div>
    </a>
</div>
""", unsafe_allow_html=True)

# ========== LAI CALCULATION ==========
risk_enhancers = (smoke == "Current") or mets or fh_fh or (lpa is not None and lpa > 50) or (apob is not None and apob > 130)
if ascvd or ckd or (diabetes == "Yes" and duration is not None and duration >= 10):
    lai = "Very High"
elif diabetes == "Yes" or risk_enhancers:
    lai = "High"
elif prem_ascvd or fh_dm or fh_htn:
    lai = "Moderate"
else:
    lai = "Low"

# ========== RISK PANEL ==========
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.header("🎯 Risk Stratification Panel")
st.markdown("")

cols = st.columns(3)

# AHA PREVENT card
with cols[0]:
    if aha_cat:
        cat_class = aha_cat.lower().replace(" ", "")
        st.markdown(
            f'<div class="risk-card risk-{cat_class}">'
            f'<h3 style="margin:0;color:{TEXT_PRIMARY};">AHA PREVENT</h3>'
            f'<h1 style="margin:0.5rem 0;color:{TEXT_PRIMARY};">{aha_cat}</h1>'
            f'<p style="margin:0;font-size:1.2rem;font-weight:600;color:{TEXT_PRIMARY};">{aha}%</p>'
            f'</div>', unsafe_allow_html=True
        )
        if aha_cat != "Low":
            factors = get_contributing_factors_aha(age, sex, tc, hdl, sbp, antihtn, diabetes, smoke)
            if factors:
                st.markdown(
                    f'<div class="contributing-factors">'
                    f'<div class="factor-title">Contributing Factors:</div>' +
                    "".join(f'<div class="factor-item">{f}</div>' for f in factors[:5]) +
                    '</div>', unsafe_allow_html=True
                )
    else:
        st.markdown(
            f'<div class="risk-card risk-unavailable">'
            f'<h3 style="margin:0;color:{TEXT_PRIMARY};">AHA PREVENT</h3>'
            f'<p style="margin:0.5rem 0;color:{TEXT_SECONDARY};">Not calculable</p>'
            f'</div>', unsafe_allow_html=True
        )

# QRISK3 card
with cols[1]:
    if qrisk_cat:
        cat_class = qrisk_cat.lower().replace(" ", "")
        st.markdown(
            f'<div class="risk-card risk-{cat_class}">'
            f'<h3 style="margin:0;color:{TEXT_PRIMARY};">QRISK3</h3>'
            f'<h1 style="margin:0.5rem 0;color:{TEXT_PRIMARY};">{qrisk_cat}</h1>'
            f'<p style="margin:0;font-size:1.2rem;font-weight:600;color:{TEXT_PRIMARY};">{qrisk}%</p>'
            f'</div>', unsafe_allow_html=True
        )
        if qrisk_cat != "Low":
            factors = get_contributing_factors_qrisk(age, sex, smoke, diabetes, bmi, sbp, tc_hdl_ratio, prem_ascvd, ckd, atrial_fib, rheumatoid_arthritis, eth)
            if factors:
                st.markdown(
                    f'<div class="contributing-factors">'
                    f'<div class="factor-title">Contributing Factors:</div>' +
                    "".join(f'<div class="factor-item">{f}</div>' for f in factors[:5]) +
                    '</div>', unsafe_allow_html=True
                )
    else:
        st.markdown(
            f'<div class="risk-card risk-unavailable">'
            f'<h3 style="margin:0;color:{TEXT_PRIMARY};">QRISK3</h3>'
            f'<p style="margin:0.5rem 0;color:{TEXT_SECONDARY};">Not calculable</p>'
            f'</div>', unsafe_allow_html=True
        )

# LAI card
with cols[2]:
    if lai:
        cat_class = lai.lower().replace(" ", "")
        st.markdown(
            f'<div class="risk-card risk-{cat_class}">'
            f'<h3 style="margin:0;color:{TEXT_PRIMARY};">LAI Risk</h3>'
            f'<h1 style="margin:0.5rem 0;color:{TEXT_PRIMARY};">{lai}</h1>'
            f'<p style="margin:0;font-size:0.9rem;font-style:italic;color:{TEXT_SECONDARY};">Lipid Association of India</p>'
            f'</div>', unsafe_allow_html=True
        )
        if lai != "Low":
            factors = get_contributing_factors_lai(ascvd, ckd, diabetes, duration, smoke, mets, fh_fh, lpa, apob, prem_ascvd, fh_dm, fh_htn, ldl)
            if factors:
                st.markdown(
                    f'<div class="contributing-factors">'
                    f'<div class="factor-title">Contributing Factors:</div>' +
                    "".join(f'<div class="factor-item">{f}</div>' for f in factors[:5]) +
                    '</div>', unsafe_allow_html=True
                )
    else:
        st.markdown(
            f'<div class="risk-card risk-unavailable">'
            f'<h3 style="margin:0;color:{TEXT_PRIMARY};">LAI Risk</h3>'
            f'<p style="margin:0.5rem 0;color:{TEXT_SECONDARY};">Unavailable</p>'
            f'</div>', unsafe_allow_html=True
        )

# ========== TREATMENT RECOMMENDATIONS ==========
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.header("📋 Treatment Recommendations by Guidelines")
st.markdown("")

tab1, tab2, tab3 = st.tabs(["AHA PREVENT", "QRISK3", "LAI 2023"])

with tab1:
    if aha_cat:
        recs = get_aha_recommendations(aha_cat, aha)
        st.subheader(f"AHA PREVENT Recommendations ({aha_cat} Risk)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Statin Therapy:** {recs['statin']}")
            st.markdown(f"**LDL-C Target:** {recs['ldl_target']}")
            st.markdown(f"**Non-HDL-C Target:** {recs['non_hdl_target']}")
        with col2:
            st.markdown(f"**Lifestyle:** {recs['lifestyle']}")
            st.markdown(f"**Monitoring:** {recs['monitoring']}")
    else:
        st.info("AHA PREVENT score not calculable with current data.")

with tab2:
    if qrisk_cat:
        recs = get_qrisk_recommendations(qrisk_cat, qrisk)
        st.subheader(f"QRISK3 Recommendations ({qrisk_cat} Risk)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Statin Therapy:** {recs['statin']}")
            st.markdown(f"**LDL-C Target:** {recs['ldl_target']}")
            st.markdown(f"**Non-HDL-C Target:** {recs['non_hdl_target']}")
        with col2:
            st.markdown(f"**Lifestyle:** {recs['lifestyle']}")
            st.markdown(f"**Monitoring:** {recs['monitoring']}")
    else:
        st.info("QRISK3 score not calculable with current data.")

with tab3:
    recs = get_lai_recommendations(lai)
    st.subheader(f"LAI 2023 Recommendations ({lai} Risk)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Statin Therapy:** {recs['statin']}")
        st.markdown(f"**LDL-C Target:** {recs['ldl_target']}")
        st.markdown(f"**Non-HDL-C Target:** {recs['non_hdl_target']}")
        st.markdown(f"**ApoB Target:** {recs['apob_target']}")
    with col2:
        st.markdown(f"**Lifestyle:** {recs['lifestyle']}")
        st.markdown(f"**Monitoring:** {recs['monitoring']}")

# ========== UNIFIED RECOMMENDATION ==========
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.header("🤖 Unified Clinical Recommendation")
st.markdown("")

with st.spinner("Generating comprehensive treatment recommendation..."):
    unified_summary = generate_fallback_summary(aha_cat, qrisk_cat, lai)
    st.markdown(unified_summary)

st.markdown("")
st.info("💡 **Note:** This unified recommendation synthesizes all three risk assessment tools and provides evidence-based guidance. Please use clinical judgment and consider individual patient factors.")

st.markdown("")
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.caption("*This tool is intended for clinical decision support based on AHA, QRISK3, and LAI 2023 Guidelines. All treatment decisions should be made through shared decision-making with the patient.*")
