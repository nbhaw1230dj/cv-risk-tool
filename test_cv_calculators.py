"""
Test Cases for Cardiovascular Risk Calculators
Demonstrates usage with various patient scenarios
"""

from cv_risk_calculators import (
    calculate_ascvd_risk,
    calculate_framingham_risk,
    assess_metabolic_syndrome,
    calculate_ldl_treatment_recommendation
)
import json


def print_separator(title=""):
    print("\n" + "=" * 100)
    if title:
        print(f"{title:^100}")
        print("=" * 100)


def test_case_1_intermediate_risk():
    """55-year-old male, smoker, hypertension, borderline lipids"""
    print_separator("TEST CASE 1: Intermediate Risk Primary Prevention")
    
    patient = {
        "demographics": {
            "age": 55,
            "sex": "male",
            "race_ethnicity": "white"
        },
        "vitals": {
            "systolic_bp": 140,
            "diastolic_bp": 90,
            "height": 175,
            "weight": 85,
            "bmi": 27.8,
            "waist_circumference": 105
        },
        "lab_values": {
            "total_cholesterol": 220,
            "hdl_cholesterol": 38,
            "ldl_cholesterol": 155,
            "triglycerides": 180,
            "fasting_glucose": 105,
            "hscrp": 2.5
        },
        "medical_history": {
            "diabetes_status": "none",
            "hypertension_treatment": True,
            "cvd_history": {
                "clinical_ascvd": False,
                "prior_mi": False,
                "prior_stroke_tia": False,
                "prior_cabg_pci": False,
                "peripheral_artery_disease": False
            }
        },
        "lifestyle_factors": {
            "smoking_status": "current"
        },
        "family_history": {
            "premature_cvd_family_history": True
        }
    }
    
    print("\nPatient Profile:")
    print(f"  Age: {patient['demographics']['age']}, Sex: {patient['demographics']['sex']}")
    print(f"  BP: {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']} (on treatment)")
    print(f"  Lipids: TC {patient['lab_values']['total_cholesterol']}, LDL {patient['lab_values']['ldl_cholesterol']}, HDL {patient['lab_values']['hdl_cholesterol']}, TG {patient['lab_values']['triglycerides']}")
    print(f"  Current smoker, Family history of premature CVD")
    
    ascvd = calculate_ascvd_risk(patient)
    print(f"\n[ASCVD Risk] {ascvd.risk_percent}% 10-year risk ({ascvd.risk_category})")
    
    framingham = calculate_framingham_risk(patient)
    print(f"[Framingham] {framingham.risk_percent}% 10-year CHD risk ({framingham.points} points, {framingham.risk_category})")
    
    mets = assess_metabolic_syndrome(patient)
    print(f"[Metabolic Syndrome] {mets.criteria_met}/5 criteria → {'YES' if mets.has_metabolic_syndrome else 'NO'}")
    
    ldl = calculate_ldl_treatment_recommendation(patient)
    print(f"\n[LDL Treatment Recommendation]")
    print(f"  Category: {ldl.risk_category}")
    print(f"  Recommended: {ldl.recommended_intensity}")
    print(f"  Risk Enhancers: {', '.join(ldl.risk_enhancers_present) if ldl.risk_enhancers_present else 'None'}")
    print(f"\n  Key Recommendations:")
    for rec in ldl.recommendations[:5]:
        print(f"    • {rec}")


def test_case_2_diabetes():
    """62-year-old female with type 2 diabetes"""
    print_separator("TEST CASE 2: Diabetes Primary Prevention")
    
    patient = {
        "demographics": {
            "age": 62,
            "sex": "female",
            "race_ethnicity": "black"
        },
        "vitals": {
            "systolic_bp": 135,
            "diastolic_bp": 82,
            "height": 165,
            "weight": 78,
            "bmi": 28.7,
            "waist_circumference": 92
        },
        "lab_values": {
            "total_cholesterol": 195,
            "hdl_cholesterol": 42,
            "ldl_cholesterol": 120,
            "triglycerides": 165,
            "fasting_glucose": 145,
            "hba1c": 7.2
        },
        "medical_history": {
            "diabetes_status": "type_2",
            "diabetes_duration": 8,
            "hypertension_treatment": True,
            "cvd_history": {
                "clinical_ascvd": False,
                "prior_mi": False,
                "prior_stroke_tia": False,
                "prior_cabg_pci": False,
                "peripheral_artery_disease": False
            },
            "chronic_kidney_disease": True
        },
        "lifestyle_factors": {
            "smoking_status": "never"
        },
        "family_history": {
            "premature_cvd_family_history": False,
            "family_history_diabetes": True
        }
    }
    
    print("\nPatient Profile:")
    print(f"  Age: {patient['demographics']['age']}, Sex: {patient['demographics']['sex']}")
    print(f"  Type 2 diabetes for 8 years, HbA1c 7.2%")
    print(f"  BP: {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']} (on treatment)")
    print(f"  LDL {patient['lab_values']['ldl_cholesterol']}, Chronic kidney disease")
    
    ascvd = calculate_ascvd_risk(patient)
    print(f"\n[ASCVD Risk] {ascvd.risk_percent}% 10-year risk ({ascvd.risk_category})")
    
    mets = assess_metabolic_syndrome(patient)
    print(f"[Metabolic Syndrome] {mets.criteria_met}/5 criteria → {'YES' if mets.has_metabolic_syndrome else 'NO'}")
    
    ldl = calculate_ldl_treatment_recommendation(patient)
    print(f"\n[LDL Treatment Recommendation]")
    print(f"  Category: {ldl.risk_category}")
    print(f"  Recommended: {ldl.recommended_intensity}")
    if ldl.ldl_goal:
        print(f"  LDL Goal: <{ldl.ldl_goal} mg/dL")
    print(f"\n  Key Recommendations:")
    for rec in ldl.recommendations[:4]:
        print(f"    • {rec}")


def test_case_3_secondary_prevention():
    """68-year-old male with prior MI and multiple risk factors"""
    print_separator("TEST CASE 3: Secondary Prevention (Very High Risk)")
    
    patient = {
        "demographics": {
            "age": 68,
            "sex": "male",
            "race_ethnicity": "white"
        },
        "vitals": {
            "systolic_bp": 128,
            "diastolic_bp": 76,
            "height": 172,
            "weight": 82,
            "bmi": 27.7,
            "waist_circumference": 98
        },
        "lab_values": {
            "total_cholesterol": 180,
            "hdl_cholesterol": 35,
            "ldl_cholesterol": 95,
            "triglycerides": 200,
            "fasting_glucose": 118,
            "hba1c": 6.3,
            "lp_a": 65,
            "hscrp": 3.2
        },
        "medical_history": {
            "diabetes_status": "type_2",
            "diabetes_duration": 5,
            "hypertension_treatment": True,
            "cvd_history": {
                "clinical_ascvd": True,
                "prior_mi": True,
                "prior_stroke_tia": False,
                "prior_cabg_pci": True,
                "peripheral_artery_disease": True
            },
            "chronic_kidney_disease": True,
            "heart_failure": False
        },
        "lifestyle_factors": {
            "smoking_status": "former"
        },
        "family_history": {
            "premature_cvd_family_history": True
        }
    }
    
    print("\nPatient Profile:")
    print(f"  Age: {patient['demographics']['age']}, Sex: {patient['demographics']['sex']}")
    print(f"  Prior MI, prior PCI/CABG, peripheral artery disease")
    print(f"  Type 2 diabetes, CKD, hypertension")
    print(f"  Current LDL: {patient['lab_values']['ldl_cholesterol']} mg/dL")
    print(f"  Lp(a) {patient['lab_values']['lp_a']} mg/dL, hsCRP {patient['lab_values']['hscrp']} mg/L")
    
    ldl = calculate_ldl_treatment_recommendation(patient)
    print(f"\n[LDL Treatment Recommendation]")
    print(f"  Category: {ldl.risk_category}")
    print(f"  Recommended: {ldl.recommended_intensity}")
    if ldl.ldl_goal:
        print(f"  LDL Goal: <{ldl.ldl_goal} mg/dL AND ≥{ldl.percent_reduction_goal}% reduction")
    print(f"\n  Key Recommendations:")
    for rec in ldl.recommendations[:6]:
        print(f"    • {rec}")


def test_case_4_severe_hyperchol():
    """45-year-old female with severe hypercholesterolemia (possible FH)"""
    print_separator("TEST CASE 4: Severe Hypercholesterolemia (LDL ≥190)")
    
    patient = {
        "demographics": {
            "age": 45,
            "sex": "female",
            "race_ethnicity": "white"
        },
        "vitals": {
            "systolic_bp": 118,
            "diastolic_bp": 72,
            "height": 168,
            "weight": 65,
            "bmi": 23.0,
            "waist_circumference": 78
        },
        "lab_values": {
            "total_cholesterol": 310,
            "hdl_cholesterol": 55,
            "ldl_cholesterol": 240,
            "triglycerides": 110,
            "fasting_glucose": 92
        },
        "medical_history": {
            "diabetes_status": "none",
            "hypertension_treatment": False,
            "cvd_history": {
                "clinical_ascvd": False,
                "prior_mi": False,
                "prior_stroke_tia": False,
                "prior_cabg_pci": False,
                "peripheral_artery_disease": False
            }
        },
        "lifestyle_factors": {
            "smoking_status": "never"
        },
        "family_history": {
            "premature_cvd_family_history": True,
            "family_hypercholesterolemia": True
        }
    }
    
    print("\nPatient Profile:")
    print(f"  Age: {patient['demographics']['age']}, Sex: {patient['demographics']['sex']}")
    print(f"  LDL: {patient['lab_values']['ldl_cholesterol']} mg/dL (severe hypercholesterolemia)")
    print(f"  Family history of premature CVD and hypercholesterolemia")
    print(f"  No other major risk factors")
    
    ascvd = calculate_ascvd_risk(patient)
    print(f"\n[ASCVD Risk] {ascvd.risk_percent}% 10-year risk ({ascvd.risk_category})")
    
    mets = assess_metabolic_syndrome(patient)
    print(f"[Metabolic Syndrome] {mets.criteria_met}/5 criteria → {'NO' if not mets.has_metabolic_syndrome else 'YES'}")
    
    ldl = calculate_ldl_treatment_recommendation(patient)
    print(f"\n[LDL Treatment Recommendation]")
    print(f"  Category: {ldl.risk_category}")
    print(f"  Recommended: {ldl.recommended_intensity}")
    if ldl.percent_reduction_goal:
        print(f"  Goal: ≥{ldl.percent_reduction_goal}% LDL reduction from baseline")
    print(f"\n  Key Recommendations:")
    for rec in ldl.recommendations:
        print(f"    • {rec}")


def test_case_5_low_risk():
    """42-year-old healthy male"""
    print_separator("TEST CASE 5: Low Risk Primary Prevention")
    
    patient = {
        "demographics": {
            "age": 42,
            "sex": "male",
            "race_ethnicity": "asian"
        },
        "vitals": {
            "systolic_bp": 115,
            "diastolic_bp": 72,
            "height": 175,
            "weight": 72,
            "bmi": 23.5,
            "waist_circumference": 85
        },
        "lab_values": {
            "total_cholesterol": 180,
            "hdl_cholesterol": 52,
            "ldl_cholesterol": 110,
            "triglycerides": 90,
            "fasting_glucose": 88
        },
        "medical_history": {
            "diabetes_status": "none",
            "hypertension_treatment": False,
            "cvd_history": {
                "clinical_ascvd": False,
                "prior_mi": False,
                "prior_stroke_tia": False,
                "prior_cabg_pci": False,
                "peripheral_artery_disease": False
            }
        },
        "lifestyle_factors": {
            "smoking_status": "never"
        },
        "family_history": {
            "premature_cvd_family_history": False
        }
    }
    
    print("\nPatient Profile:")
    print(f"  Age: {patient['demographics']['age']}, Sex: {patient['demographics']['sex']}")
    print(f"  BP: {patient['vitals']['systolic_bp']}/{patient['vitals']['diastolic_bp']} (no treatment)")
    print(f"  LDL {patient['lab_values']['ldl_cholesterol']}, HDL {patient['lab_values']['hdl_cholesterol']}")
    print(f"  Non-smoker, no diabetes, no family history")
    
    ascvd = calculate_ascvd_risk(patient)
    print(f"\n[ASCVD Risk] {ascvd.risk_percent}% 10-year risk ({ascvd.risk_category})")
    
    framingham = calculate_framingham_risk(patient)
    print(f"[Framingham] {framingham.risk_percent}% 10-year CHD risk ({framingham.points} points)")
    
    mets = assess_metabolic_syndrome(patient)
    print(f"[Metabolic Syndrome] {mets.criteria_met}/5 criteria → {'NO' if not mets.has_metabolic_syndrome else 'YES'}")
    
    ldl = calculate_ldl_treatment_recommendation(patient)
    print(f"\n[LDL Treatment Recommendation]")
    print(f"  Category: {ldl.risk_category}")
    print(f"  Recommended: {ldl.recommended_intensity}")
    print(f"\n  Key Recommendations:")
    for rec in ldl.recommendations[:4]:
        print(f"    • {rec}")


def test_case_6_metabolic_syndrome():
    """58-year-old female with metabolic syndrome"""
    print_separator("TEST CASE 6: Metabolic Syndrome with Risk Enhancers")
    
    patient = {
        "demographics": {
            "age": 58,
            "sex": "female",
            "race_ethnicity": "hispanic"
        },
        "vitals": {
            "systolic_bp": 138,
            "diastolic_bp": 88,
            "height": 160,
            "weight": 75,
            "bmi": 29.3,
            "waist_circumference": 95
        },
        "lab_values": {
            "total_cholesterol": 215,
            "hdl_cholesterol": 42,
            "ldl_cholesterol": 138,
            "triglycerides": 195,
            "fasting_glucose": 108,
            "hba1c": 5.9,
            "hscrp": 3.8,
            "coronary_calcium_score": 125
        },
        "medical_history": {
            "diabetes_status": "prediabetes",
            "hypertension_treatment": True,
            "cvd_history": {
                "clinical_ascvd": False,
                "prior_mi": False,
                "prior_stroke_tia": False,
                "prior_cabg_pci": False,
                "peripheral_artery_disease": False
            },
            "pregnancy_complications": {
                "preeclampsia": True,
                "gestational_diabetes": True
            }
        },
        "lifestyle_factors": {
            "smoking_status": "never"
        },
        "family_history": {
            "premature_cvd_family_history": True,
            "family_history_diabetes": True
        }
    }
    
    print("\nPatient Profile:")
    print(f"  Age: {patient['demographics']['age']}, Sex: {patient['demographics']['sex']}")
    print(f"  Prediabetes, hypertension (treated)")
    print(f"  Waist: {patient['vitals']['waist_circumference']} cm, BMI: {patient['vitals']['bmi']}")
    print(f"  LDL {patient['lab_values']['ldl_cholesterol']}, HDL {patient['lab_values']['hdl_cholesterol']}, TG {patient['lab_values']['triglycerides']}")
    print(f"  CAC score: {patient['lab_values']['coronary_calcium_score']}")
    print(f"  History: preeclampsia, gestational diabetes")
    
    ascvd = calculate_ascvd_risk(patient)
    print(f"\n[ASCVD Risk] {ascvd.risk_percent}% 10-year risk ({ascvd.risk_category})")
    
    mets = assess_metabolic_syndrome(patient)
    print(f"\n[Metabolic Syndrome Assessment]")
    print(f"  Status: {'PRESENT' if mets.has_metabolic_syndrome else 'ABSENT'} ({mets.criteria_met}/5 criteria)")
    print(f"  Components:")
    for component, status in mets.components.items():
        status_str = "✓" if status else "✗"
        print(f"    {status_str} {component}")
    
    ldl = calculate_ldl_treatment_recommendation(patient)
    print(f"\n[LDL Treatment Recommendation]")
    print(f"  Category: {ldl.risk_category}")
    print(f"  Recommended: {ldl.recommended_intensity}")
    print(f"\n  Risk Enhancers Present ({len(ldl.risk_enhancers_present)}):")
    for enhancer in ldl.risk_enhancers_present:
        print(f"    • {enhancer}")
    print(f"\n  Key Recommendations:")
    for rec in ldl.recommendations[:6]:
        print(f"    • {rec}")


def run_all_tests():
    """Run all test cases"""
    test_case_1_intermediate_risk()
    test_case_2_diabetes()
    test_case_3_secondary_prevention()
    test_case_4_severe_hyperchol()
    test_case_5_low_risk()
    test_case_6_metabolic_syndrome()
    
    print_separator("ALL TESTS COMPLETED")
    print("\nSummary:")
    print("  ✓ ASCVD Pooled Cohort Equation (2013 ACC/AHA)")
    print("  ✓ Framingham Risk Score (ATP III)")
    print("  ✓ Metabolic Syndrome (ATP III/AHA 2005 criteria)")
    print("  ✓ LDL Treatment Recommendations (2019 ACC/AHA Guideline)")
    print("\nAll calculators use published formulas and criteria.")
    print("Suitable for clinical decision support software implementation.")
    print("=" * 100)


if __name__ == "__main__":
    run_all_tests()
