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
    BG_PAGE = "#0f1117"
    BG_SECONDARY = "#171a23"
    BG_INPUT = "#1f2430"
    TEXT_PRIMARY = "#e8eaf0"
    TEXT_SECONDARY = "#9aa0b8"
    TEXT_MUTED = "#6b7280"
    BORDER_COLOR = "#2b3142"
    ACCENT = "#4c9ef8"
    ACCENT_DARK = "#3a82d6"
    TOOLBAR_BG = "#0f1117"
    BTN_PRIMARY_BG = "#4c9ef8"
    BTN_PRIMARY_HOVER = "#3a82d6"
    BTN_SECONDARY_BG = "#1f2430"
    BTN_SECONDARY_BORDER = "#4c9ef8"
    BTN_SECONDARY_COLOR = "#e8eaf0"
    RESET_BTN_BG = "#1f2430"
    RESET_BTN_COLOR = "#e8eaf0"
    RESET_BTN_BORDER = "#4c9ef8"
    THEME_BTN_BG = "#4c9ef8"
    THEME_BTN_COLOR = "#ffffff"
    THEME_BTN_BORDER = "#4c9ef8"
    TOGGLE_ICON = "☀"
else:
    BG_PAGE = "#f4f6fb"
    BG_SECONDARY = "#ffffff"
    BG_INPUT = "#ffffff"
    TEXT_PRIMARY = "#0f172a"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#64748b"
    BORDER_COLOR = "#e2e8f0"
    ACCENT = "#2563eb"
    ACCENT_DARK = "#1e40af"
    TOOLBAR_BG = "#f4f6fb"
    BTN_PRIMARY_BG = "#2563eb"
    BTN_PRIMARY_HOVER = "#1e40af"
    BTN_SECONDARY_BG = "#ffffff"
    BTN_SECONDARY_BORDER = "#d1d5db"
    BTN_SECONDARY_COLOR = "#374151"
    RESET_BTN_BG = "#ffffff"
    RESET_BTN_COLOR = "#374151"
    RESET_BTN_BORDER = "#d1d5db"
    THEME_BTN_BG = "#2563eb"
    THEME_BTN_COLOR = "#ffffff"
    THEME_BTN_BORDER = "#2563eb"
    TOGGLE_ICON = "🌙"

# ========== CSS INJECTION ==========
st.markdown(f"""
<style>

/* ---- Remove Streamlit chrome & top white bar ---- */
header, footer, #MainMenu, .stDeployButton,
[data-testid="stToolbar"] {{
    display: none !important;
}}

html, body {{
    background-color: {BG_PAGE} !important;
}}

.stApp {{
    background-color: {BG_PAGE} !important;
}}

[data-testid="stAppViewContainer"] {{
    background-color: {BG_PAGE} !important;
}}

.block-container {{
    padding-top: 3.2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
    background-color: {BG_PAGE} !important;
}}

/* ---- Typography ---- */
.main-title {{
    font-size: clamp(1.8rem, 3.2vw, 2.4rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    color: {TEXT_PRIMARY};
    border-bottom: 3px solid {ACCENT};
    padding-bottom: 0.6rem;
    margin-bottom: 1.2rem;
}}

.section-sep-label {{
    font-size: 0.95rem;
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
    margin: 1.8rem 0 0.8rem 0;
}}

/* ---- Buttons ---- */
.stButton > button {{
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s ease !important;
}}

.cv-reset-btn .stButton > button {{
    background-color: {RESET_BTN_BG} !important;
    color: {RESET_BTN_COLOR} !important;
    border: 1.5px solid {RESET_BTN_BORDER} !important;
}}

.cv-reset-btn .stButton > button:hover {{
    border-color: {ACCENT} !important;
    color: {ACCENT} !important;
}}

.cv-theme-btn .stButton > button {{
    background-color: {THEME_BTN_BG} !important;
    color: {THEME_BTN_COLOR} !important;
    border: 1.5px solid {THEME_BTN_BORDER} !important;
}}

.cv-theme-btn .stButton > button:hover {{
    background-color: {ACCENT_DARK} !important;
    border-color: {ACCENT_DARK} !important;
}}

.stButton > button:not(.cv-reset-btn button):not(.cv-theme-btn button) {{
    background-color: {BTN_PRIMARY_BG} !important;
    color: #ffffff !important;
}}

.stButton > button:hover {{
    box-shadow: none !important;
    transform: none !important;
}}

/* ---- Inputs ---- */
input, select, textarea {{
    background-color: {BG_INPUT} !important;
    color: {TEXT_PRIMARY} !important;
    border: 1.5px solid {BORDER_COLOR} !important;
    border-radius: 6px !important;
}}

.stNumberInput input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {ACCENT}22 !important;
}}

/* ---- Metrics ---- */
[data-testid="stMetric"] {{
    background: {BG_SECONDARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 10px;
    padding: 1rem;
}}

[data-testid="stMetricValue"] {{
    font-size: 1.6rem !important;
    font-weight: 800 !important;
    color: {TEXT_PRIMARY} !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 0.85rem !important;
    color: {TEXT_SECONDARY} !important;
}}

/* ---- Reference Pills ---- */
.cv-ref-pill {{
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.5rem 1rem;
    background: {BTN_SECONDARY_BG};
    color: {BTN_SECONDARY_COLOR} !important;
    border: 1.5px solid {BTN_SECONDARY_BORDER};
    text-decoration: none !important;
    transition: all 0.15s ease;
}}

.cv-ref-pill:hover {{
    border-color: {ACCENT};
    color: {ACCENT} !important;
}}

/* ---- Responsive ---- */
@media (max-width: 900px) {{
    .main-title {{
        font-size: 1.9rem;
    }}
}}

</style>
""", unsafe_allow_html=True)

# ==================== HEADER ====================

header_cols = st.columns([2, 1])

with header_cols[0]:
    st.markdown(f'<div class="main-title">🫀 Cardiovascular Risk Assessment Tool</div>', unsafe_allow_html=True)

with header_cols[1]:
    ref_row = st.columns(2)
    with ref_row[0]:
        st.markdown(
            '<a href="https://professional.heart.org/en/guidelines-and-statements/prevent-calculator" target="_blank" class="cv-ref-pill">↗ AHA PREVENT</a>',
            unsafe_allow_html=True
        )
    with ref_row[1]:
        st.markdown(
            '<a href="https://qrisk.org/" target="_blank" class="cv-ref-pill">↗ QRISK3</a>',
            unsafe_allow_html=True
        )

control_cols = st.columns([3, 1, 1])

with control_cols[1]:
    st.markdown('<div class="cv-reset-btn">', unsafe_allow_html=True)
    if st.button("↺ Reset", key="btn_reset"):
        reset_all()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with control_cols[2]:
    st.markdown('<div class="cv-theme-btn">', unsafe_allow_html=True)
    st.button(f"{TOGGLE_ICON} {'Light Mode' if is_dark else 'Dark Mode'}",
              key="btn_theme",
              on_click=toggle_theme)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1.2rem;"></div>', unsafe_allow_html=True)

# ==================== REST OF ORIGINAL APP UNCHANGED ====================
# (All original logic, calculations, risk panels, tabs,
# unified recommendation, and reference sections remain EXACTLY the same below.)
