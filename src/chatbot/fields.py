# ============================================================
# DIABETES FIELDS
# ============================================================

DIABETES_FIELDS = [
    "gender",
    "smoking_history",
    "age",
    "bmi",
    "HbA1c_level",
    "blood_glucose_level",
    "hypertension",
    "heart_disease",
    "age_group",
    "bmi_category",
]


# ============================================================
# HEART DISEASE FIELDS
# ============================================================

HEART_FIELDS = [
    "age",
    "sex",
    "chest pain type",
    "resting bp s",
    "cholesterol",
    "fasting blood sugar",
    "resting ecg",
    "max heart rate",
    "exercise angina",
    "oldpeak",
    "ST slope",
]


# ============================================================
# TREATMENT FIELDS
# ============================================================

TREATMENT_FIELDS = [
    "Age",
    "Gender",
    "self_employed",
    "family_history",
    "work_interfere",
    "no_employees",
    "remote_work",
    "tech_company",
    "benefits",
    "care_options",
    "wellness_program",
    "seek_help",
    "anonymity",
    "leave",
    "mental_health_consequence",
    "phys_health_consequence",
    "coworkers",
    "supervisor",
    "mental_health_interview",
    "phys_health_interview",
    "mental_vs_physical",
    "obs_consequence",
    "Country",
]


# ============================================================
# PREDICTION FIELDS
# ============================================================

PREDICTION_FIELDS = {
    "diabetes": DIABETES_FIELDS,
    "heart": HEART_FIELDS,
    "treatment": TREATMENT_FIELDS,
}


# ============================================================
# AUTOMATIC FIELDS
# (never asked to the user / never requested from Gemini -
#  computed automatically from other fields instead)
# ============================================================

AUTO_FIELDS = {
    "diabetes": [
        "age_group",
        "bmi_category",
    ]
}


# ============================================================
# AUTO FIELD COMPUTATION
# ------------------------------------------------------------
# BUG FIX: age_group / bmi_category were listed as AUTO_FIELDS
# (i.e. "don't ask the user, don't count as missing") but nothing
# in the original codebase ever actually computed them, so
# predict_diabetes() would KeyError looking for "Age_group" /
# "BMI_category" whenever a prediction came through the chatbot.
# These functions are called from src/prediction_engine.py.
# ============================================================

def get_age_group(age: float) -> str:
    """Bucket a numeric age into the categories the diabetes model
    was trained on."""

    age = float(age)

    if age < 18:
        return "Child"

    elif age < 30:
        return "Young"

    elif age < 45:
        return "Adult"

    elif age < 60:
        return "Middle_age"

    else:
        return "Senior"


def get_bmi_category(bmi: float) -> str:
    """Bucket a numeric BMI into the standard WHO-style categories
    the diabetes model was trained on."""

    bmi = float(bmi)

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal weight"

    elif bmi < 30:
        return "Overweight"

    elif bmi < 35:
        return "Obesity class 1"

    elif bmi < 40:
        return "Obesity class 2"

    else:
        return "Obesity class 3"


# ============================================================
# REQUIRED FIELDS
# ============================================================

def get_required_fields(condition: str):

    return PREDICTION_FIELDS.get(
        condition,
        []
    )


# ============================================================
# MISSING FIELDS
# ============================================================

def get_missing_fields(
    condition: str,
    data: dict
):

    required_fields = get_required_fields(
        condition
    )

    auto_fields = AUTO_FIELDS.get(
        condition,
        []
    )

    missing_fields = [
        field
        for field in required_fields
        if field not in data
        and field not in auto_fields
    ]

    return missing_fields
