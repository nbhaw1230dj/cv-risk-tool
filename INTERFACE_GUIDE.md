# CV Risk Assessment App - Interface Guide

## Application Overview

The Cardiovascular Risk Assessment application provides a clean, medical-grade interface for calculating patient cardiovascular risk scores based on ACC/AHA 2019 guidelines.

## Interface Layout

### 1. Header Section
- **Title**: "❤️ Cardiovascular Risk Assessment"
- **Subtitle**: Evidence-based risk calculator using ACC/AHA 2019 Guidelines
- Professional medical color scheme (blue/white)

### 2. Patient Data Entry Form

The form is organized into 6 logical sections:

#### 📋 Demographics
- **Age** (18-120 years)
- **Sex** (Male/Female)
- **Race/Ethnicity** (White, Black/African American, Hispanic, Asian, Other)
- **Patient ID** (optional)

#### 🩺 Vital Signs
- **Systolic BP** (mmHg)
- **Diastolic BP** (mmHg)
- **Height** (cm)
- **Weight** (kg)
- **Waist Circumference** (cm)
- **Auto-calculated BMI** displayed immediately

#### 🧪 Laboratory Values

**Required Labs:**
- Total Cholesterol (mg/dL)
- HDL Cholesterol (mg/dL)
- LDL Cholesterol (mg/dL)
- Triglycerides (mg/dL)
- Fasting Glucose (mg/dL)

**Optional Labs (for risk enhancement):**
- HbA1c (%)
- hsCRP (mg/L) - with tooltip: "Risk enhancer if ≥2.0"
- Lp(a) (mg/dL) - with tooltip: "Risk enhancer if ≥50"
- CAC Score (Agatston units) - with tooltip: "Coronary Artery Calcium score"

#### 📝 Medical History

**Diabetes & Treatment:**
- Diabetes Status dropdown
- Diabetes Duration (if applicable)
- On Hypertension Treatment (checkbox)
- Chronic Kidney Disease (checkbox)

**Prior Cardiovascular Events:**
- Prior MI (checkbox)
- Prior Stroke/TIA (checkbox)
- Prior PCI/CABG (checkbox)
- Peripheral Artery Disease (checkbox)

**Other Conditions:**
- Heart Failure
- Atrial Fibrillation
- Rheumatoid Arthritis
- Psoriasis
- HIV Infection
- Systemic Lupus Erythematosus

**Women's Health History** (displayed only if sex = Female):
- Premature Menopause (<40 years)
- History of Preeclampsia
- History of Gestational Diabetes

#### 👨‍👩‍👧‍👦 Family History
- Premature CVD in First-Degree Relative (with tooltip: "Male <55 or Female <65")
- Family History of Diabetes

#### 🚭 Lifestyle Factors
- **Smoking Status** (Never/Former/Current Smoker)
- **Pack-Years** (if smoker)

### 3. Calculate Button
- Large, prominent blue button: "🔍 Calculate Risk Assessment"
- Full width for easy clicking
- Triggers all calculations

## Results Display

### Risk Score Cards (3 columns)

#### ASCVD 10-Year Risk
- **Large percentage display** (e.g., "15.2%")
- **Color-coded background:**
  - 🟢 Green: Low (<5%)
  - 🟡 Yellow: Borderline (5-7.4%)
  - 🟠 Orange: Intermediate (7.5-19.9%)
  - 🔴 Red: High (≥20%)
- **Risk category label**
- **Clinical interpretation** below card

#### Framingham CHD Risk
- **Percentage and point score**
- **Color-coded by risk level**
- Same color scheme as ASCVD

#### Metabolic Syndrome
- **PRESENT or ABSENT**
- **Criteria count** (e.g., "3/5 criteria met")
- **Component breakdown** with checkmarks:
  - ✓ Elevated waist circumference
  - ✓ Elevated triglycerides
  - ✓ Reduced HDL cholesterol
  - ✗ Elevated blood pressure
  - ✗ Elevated fasting glucose

### 💊 Treatment Recommendations Section

**Left Column:**
- Risk Category (e.g., "Primary Prevention Intermediate Risk")
- Recommended Treatment (e.g., "Moderate-intensity statin")
- LDL Goal (if applicable)
- Target Reduction percentage

**Right Column:**
- Current LDL metric card
- Status indicator (Above goal / At goal)

**Risk Enhancers** (if present):
- Bulleted list of all identified risk enhancers
- Examples:
  • Family history of premature ASCVD
  • hsCRP ≥2.0 mg/L
  • CAC score 125 (≥100)

**Detailed Clinical Recommendations** (expandable):
- Complete list of evidence-based recommendations
- Statin intensity guidance
- When to add ezetimibe or PCSK9 inhibitors
- Lifestyle modification recommendations

### 📄 Clinical Report Section

**Generated report includes:**
- Patient demographics summary
- All calculated risk scores with interpretation
- Metabolic syndrome status with components
- Treatment recommendations with targets
- Risk enhancers list
- Key clinical actions
- Date and guideline reference

**Action Buttons:**
- 📥 **Download Report** - saves as .txt file
- 🔄 **New Assessment** - clears form for next patient

## Color-Coded Risk System

### Visual Risk Indicators

**Low Risk** (Green background, dark green text):
- Light green (#d4edda) background
- Dark green (#155724) text
- Green left border
- Communicates: Safe, continue lifestyle

**Borderline Risk** (Yellow background, brown text):
- Light yellow (#fff3cd) background
- Brown (#856404) text
- Yellow left border
- Communicates: Caution, consider risk factors

**Intermediate Risk** (Orange background, brown text):
- Light yellow-orange background
- Brown text
- Orange left border
- Communicates: Action needed, start discussion

**High Risk** (Red background, dark red text):
- Light red (#f8d7da) background
- Dark red (#721c24) text
- Red left border
- Communicates: Immediate action, therapy indicated

## User Experience Features

### Speed & Efficiency
- **No page reloads** - all calculations instant
- **Form stays populated** - results appear below
- **One-click report download**
- **Quick reset** for next patient

### Error Prevention
- **Input validation** - age/BP/lab ranges enforced
- **Helpful tooltips** on medical terms
- **Auto-calculation** of BMI
- **Clear error messages** if data missing

### Clinical Workflow Support
- **Logical section grouping** matches clinic workflow
- **Optional fields** clearly marked
- **Conditional fields** (e.g., women's health) appear only when relevant
- **Compact layout** - entire form visible on standard screen

### Professional Design
- Medical-appropriate color palette
- Clean typography (large, readable fonts)
- Ample whitespace
- Professional iconography (❤️🩺🧪📝👨‍👩‍👧‍👦🚭💊📄)

## Example Workflow

### Typical 5-Minute Assessment

**Minute 1-2: Data Entry**
1. Open app (stays running between patients)
2. Enter age, sex, race
3. Enter vitals from MA/nurse
4. BMI auto-calculates

**Minute 2-3: Lab Values**
1. Pull up recent lab results
2. Enter cholesterol panel
3. Enter glucose/HbA1c
4. Add optional risk enhancers if available (CRP, Lp(a), CAC)

**Minute 3-4: History**
1. Check diabetes status
2. Check hypertension treatment
3. Check for prior events (MI/stroke/revasc)
4. Check family history
5. Select smoking status

**Minute 4: Calculate**
1. Click "Calculate Risk Assessment"
2. Results appear in <1 second

**Minute 5: Review & Document**
1. Review risk scores with patient
2. Discuss treatment recommendations
3. Download report
4. Copy key points to EMR
5. Click "New Assessment"

## Report Format

The downloadable report is a clean text file suitable for:
- Copy/paste into EMR
- Email to patient
- Print for patient education
- Include in referral letters

**Report filename format:**
`cv_risk_report_[PatientID]_[Date].txt`

Example:
`cv_risk_report_MRN12345_2024-02-13.txt`

## Mobile/Tablet Compatibility

- **Responsive design** - works on tablets
- **Touch-friendly** buttons and inputs
- **Scrollable** on smaller screens
- **Recommended**: Desktop/laptop for optimal experience in clinic

## Data Handling

### Privacy & Security
- **No data saved** - calculations performed locally
- **No internet connection required** after initial setup
- **No patient data sent externally**
- **No cookies or tracking**

### For Production Deployment
Consider adding:
- EMR integration for auto-population
- Secure patient database storage
- Audit logging
- Multi-user support with authentication
- Encrypted data transmission

## Technical Requirements

**Minimum System:**
- Python 3.8+
- 2GB RAM
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- No internet required (after installation)

**Optimal System:**
- Python 3.10+
- 4GB RAM
- Chrome or Edge browser
- Large monitor (≥1920x1080) for best form visibility

## Accessibility Features

- **High contrast text** for readability
- **Large click targets** for checkboxes/buttons
- **Keyboard navigation** supported
- **Clear visual hierarchy**
- **Color not sole indicator** - text labels reinforce colors

## Support & Training

### For New Users
1. Review QUICKSTART.md
2. Run test patient (see test_cv_calculators.py for examples)
3. Compare results to manual calculation
4. Practice 2-3 assessments before clinical use

### For IT/Administrators
1. Review README.md for technical details
2. Review cv_risk_calculators.py for calculation logic
3. Set up on clinic workstation
4. Configure for multi-user access if needed
5. Implement backup/audit logging as required

---

**The interface is designed to match clinical workflow, minimize clicks, and provide immediate, actionable results for cardiovascular risk assessment.**
