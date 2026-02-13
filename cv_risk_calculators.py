def safe(value):
    return value is not None

# ---------------- ASCVD (simplified placeholder)
def ascvd(patient):
    required = ["age","ldl","hdl","sbp"]
    for r in required:
        if not safe(patient.get(r)):
            return {"status":"not_calculable","reason":f"missing {r}"}

    risk = (patient["age"]*0.15) + (patient["ldl"]*0.02) - (patient["hdl"]*0.02)
    return {"status":"ok","value":f"{round(risk,1)} %"}

# ---------------- Framingham
def framingham(patient):
    if not safe(patient.get("age")) or not safe(patient.get("tc")):
        return {"status":"not_calculable","reason":"missing age or cholesterol"}
    score = patient["age"]*0.2 + patient["tc"]*0.01
    return {"status":"ok","value":f"{round(score,1)} %"}

# ---------------- QRISK (approx clinical indicator)
def qrisk(patient):
    if not safe(patient.get("age")):
        return {"status":"not_calculable","reason":"missing age"}
    score = patient["age"]*0.25
    return {"status":"ok","value":f"{round(score,1)} %"}

# ---------------- Lifetime Risk
def lifetime(patient):
    if not safe(patient.get("age")):
        return {"status":"not_calculable","reason":"missing age"}
    risk = "High" if patient["age"]>40 else "Moderate"
    return {"status":"ok","value":risk}

# ---------------- Therapy Recommendation
def therapy(patient):
    ldl = patient.get("ldl")
    statin = patient.get("statin")

    if ldl is None:
        return {"status":"not_calculable","reason":"missing LDL"}

    if statin=="No statin" and ldl>130:
        plan="Start statin"
    elif statin=="Moderate intensity" and ldl>100:
        plan="Increase intensity"
    elif statin=="High intensity" and ldl>70:
        plan="Add ezetimibe"
    else:
        plan="Continue current therapy"

    return {"status":"ok","value":plan}

# ---------------- Run All
def run_all_risk_assessments(patient):
    return {
        "ASCVD":ascvd(patient),
        "Framingham":framingham(patient),
        "QRISK":qrisk(patient),
        "Lifetime Risk":lifetime(patient),
        "Therapy Recommendation":therapy(patient)
    }