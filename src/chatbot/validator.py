import re


# ============================================================
# NUMBER WORDS
# ============================================================

NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,

    "ek": 1,
    "do": 2,
    "teen": 3,
    "char": 4,
    "chaar": 4,
    "paanch": 5,
    "panch": 5,
    "che": 6,
    "chhe": 6,
    "saat": 7,
    "aath": 8,
    "nau": 9,
    "das": 10,

    "pehla": 1,
    "pehli": 1,
    "dusra": 2,
    "doosra": 2,
    "teesra": 3,
    "chautha": 4,
}


# ============================================================
# FIELD RANGES
# ============================================================

FIELD_RANGES = {

    # Diabetes
    "age": (1, 120),
    "Age": (1, 120),
    "bmi": (10, 80),
    "HbA1c_level": (2, 20),
    "blood_glucose_level": (30, 500),

    # Heart
    "sex": (0, 1),

    # BUG FIX: was (0, 3). The heart disease schema
    # (backend/schemas/heart_dieses.py) uses Literal[1, 2, 3, 4] for
    # chest_pain_type, so a chatbot-collected value of e.g. 0 or 3
    # would pass this range check but then be rejected (or silently
    # wrong) once it reached the model. Aligned to 1-4.
    "chest pain type": (1, 4),

    "resting bp s": (50, 300),
    "cholesterol": (50, 700),
    "fasting blood sugar": (0, 1),
    "resting ecg": (0, 2),
    "max heart rate": (50, 250),
    "exercise angina": (0, 1),
    "oldpeak": (-5, 10),
    "ST slope": (0, 2),

}


# ============================================================
# YES / NO
# ============================================================

YES_VALUES = {
    "yes",
    "y",
    "haan",
    "ha",
    "ji",
    "jee",
    "true",
    "1",
}

NO_VALUES = {
    "no",
    "n",
    "nahi",
    "nahin",
    "na",
    "false",
    "0",
}


# ============================================================
# TREATMENT FIELD OPTIONS
# ------------------------------------------------------------
# BUG FIX: backend/schemas/treatment.py expects STRING category
# values (e.g. "Yes" / "No" / "Maybe" / "Don't know" / "Some of
# them") for all of these fields, because the trained treatment
# model's preprocessing pipeline was fit on those exact strings.
#
# The original convert_value() function lumped several of these
# fields (self_employed, remote_work, tech_company,
# mental_health_consequence, phys_health_consequence,
# mental_health_interview, phys_health_interview,
# mental_vs_physical, obs_consequence) into `yes_no_fields` and
# converted them to the integers 1/0 - which does not match what
# the schema/model expects, and would break every treatment
# prediction made through the chatbot. It also never handled
# "family_history" at all, so it passed through as a raw,
# unvalidated string.
#
# This table lists the exact allowed values (matching
# backend/schemas/treatment.py's Literal types) and is used to
# case-insensitively normalize + validate every treatment field.
# ============================================================

TREATMENT_FIELD_OPTIONS = {
    "self_employed": ["No", "Yes"],
    "family_history": ["No", "Yes"],
    "work_interfere": ["Often", "Rarely", "Never", "Sometimes", "Unknown"],
    "no_employees": [
        "1-5", "6-25", "26-100", "100-500", "500-1000", "More than 1000"
    ],
    "remote_work": ["No", "Yes"],
    "tech_company": ["Yes", "No"],
    "benefits": ["Yes", "Don't know", "No"],
    "care_options": ["Not sure", "No", "Yes"],
    "wellness_program": ["No", "Don't know", "Yes"],
    "seek_help": ["Yes", "Don't know", "No"],
    "anonymity": ["Yes", "Don't know", "No"],
    "leave": [
        "Somewhat easy", "Don't know", "Somewhat difficult",
        "Very difficult", "Very easy"
    ],
    "mental_health_consequence": ["No", "Maybe", "Yes"],
    "phys_health_consequence": ["No", "Yes", "Maybe"],
    "coworkers": ["Some of them", "No", "Yes"],
    "supervisor": ["Yes", "No", "Some of them"],
    "mental_health_interview": ["No", "Yes", "Maybe"],
    "phys_health_interview": ["Maybe", "No", "Yes"],
    "mental_vs_physical": ["Yes", "Don't know", "No"],
    "obs_consequence": ["No", "Yes"],
}


def normalize_treatment_value(field: str, value: str):
    """Case-insensitively match a free-text answer against the
    exact literal values backend/schemas/treatment.py allows for
    this field, returning the canonically-cased option (or None if
    nothing matches)."""

    options = TREATMENT_FIELD_OPTIONS.get(field)

    if not options:
        return None

    lower_value = value.strip().lower()

    # For plain Yes/No fields, accept common synonyms
    # (haan/nahi/y/n/etc.) too.
    if "Yes" in options and "No" in options:

        if lower_value in YES_VALUES:
            return "Yes"

        if lower_value in NO_VALUES:
            return "No"

    for option in options:
        if lower_value == option.lower():
            return option

    return None


# ============================================================
# TEXT NUMBER CONVERTER
# ============================================================

def word_to_number(value: str):

    text = value.strip().lower()

    # Direct numeric value
    try:
        if "." in text:
            return float(text)

        return int(text)

    except ValueError:
        pass

    # Remove common words
    text = text.replace("-", " ")
    text = text.replace(",", " ")

    # Exact word
    if text in NUMBER_WORDS:
        return NUMBER_WORDS[text]

    # Search inside sentence
    # (handles "type one", "type 1", "chest pain type one", etc.)
    words = text.split()

    for word in words:
        if word in NUMBER_WORDS:
            return NUMBER_WORDS[word]

    # Number embedded in text
    match = re.search(r"\b\d+(?:\.\d+)?\b", text)

    if match:
        number = match.group()

        if "." in number:
            return float(number)

        return int(number)

    return None


# ============================================================
# CONVERT VALUE
# ============================================================

def convert_value(field: str, value: str):

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    lower = value.lower().strip()


    # ========================================================
    # YES / NO FIELDS (genuine 1/0 integer fields only)
    # ------------------------------------------------------
    # BUG FIX: this list previously also contained several
    # treatment fields (self_employed, remote_work, tech_company,
    # mental_health_consequence, phys_health_consequence,
    # mental_health_interview, phys_health_interview,
    # mental_vs_physical, obs_consequence) which do NOT expect
    # integers - see TREATMENT_FIELD_OPTIONS above, which now
    # handles those instead.
    # ========================================================

    yes_no_fields = [
        "hypertension",
        "heart_disease",
        "fasting blood sugar",
        "exercise angina",
    ]

    if field in yes_no_fields:

        if lower in YES_VALUES:
            return 1

        if lower in NO_VALUES:
            return 0

        # Neither a recognized yes nor no value.
        # Return None (instead of falling through) so that
        # validate_value() correctly flags this as invalid,
        # rather than silently saving garbage text.
        return None


    # ========================================================
    # TREATMENT STRING-CATEGORY FIELDS
    # ========================================================

    if field in TREATMENT_FIELD_OPTIONS:
        return normalize_treatment_value(field, value)


    # ========================================================
    # GENDER
    # ========================================================

    if field in ["gender", "Gender"]:

        male_words = {"male", "m", "man", "men", "boy", "aadmi", "mard"}
        female_words = {
            "female",
            "f",
            "woman",
            "women",
            "girl",
            "aurat",
            "mahila",
        }
        other_words = {"other", "others"}

        # Exact match (fast path)
        if lower in male_words:
            return "Male"

        if lower in female_words:
            return "Female"

        if lower in other_words:
            return "Other"

        # Sentence mein embedded word dhoondo
        # (e.g. "main male hoon", "mera gender female hai")
        words = set(lower.replace(",", " ").split())

        if words & male_words:
            return "Male"

        if words & female_words:
            return "Female"

        if words & other_words:
            return "Other"

        return value


    # ========================================================
    # HEART SEX
    # ========================================================

    if field == "sex":

        male_words = {"male", "m", "man", "aadmi", "mard"}
        female_words = {"female", "f", "woman", "aurat", "mahila"}

        # Exact match (fast path)
        if lower in male_words:
            return 1

        if lower in female_words:
            return 0

        # Sentence mein embedded word dhoondo
        # (e.g. "main male hoon", "sex female hai")
        words = set(lower.replace(",", " ").split())

        if words & male_words:
            return 1

        if words & female_words:
            return 0

        number = word_to_number(value)

        if number is not None:
            return int(number)

        return None


    # ========================================================
    # SMOKING HISTORY
    # ------------------------------------------------------
    # BUG FIX: previously smoking_history fell through to the
    # DEFAULT branch and was stored exactly as the user/Gemini
    # typed it (e.g. "Never" or "NEVER"). validate_value() accepted
    # any casing, but the diabetes model's preprocessor was trained
    # on the exact lowercase/canonical strings below, so a
    # differently-cased value could be treated as an unseen
    # category. Now normalized to the canonical casing.
    # ========================================================

    if field == "smoking_history":

        allowed_smoking = [
            "never",
            "No Info",
            "current",
            "former",
            "ever",
            "not current",
        ]

        lower_map = {option.lower(): option for option in allowed_smoking}

        if lower in lower_map:
            return lower_map[lower]

        return value


    # ========================================================
    # NUMERIC FIELDS
    # ========================================================

    numeric_fields = [

        # Diabetes
        "age",
        "Age",
        "bmi",
        "HbA1c_level",
        "blood_glucose_level",

        # Heart
        "chest pain type",
        "resting bp s",
        "cholesterol",
        "resting ecg",
        "max heart rate",
        "oldpeak",
        "ST slope",
    ]

    if field in numeric_fields:

        number = word_to_number(value)

        if number is not None:

            if field in [
                "age",
                "Age",
                "chest pain type",
                "resting bp s",
                "cholesterol",
                "resting ecg",
                "max heart rate",
                "ST slope",
            ]:
                return int(number)

            return float(number)


    # ========================================================
    # DEFAULT
    # ========================================================

    return value


# ============================================================
# VALIDATION
# ============================================================

def validate_value(field: str, value):

    if value is None:
        return {
            "valid": False,
            "message": f"Please enter a valid value for {field}."
        }


    # ========================================================
    # NUMERIC RANGE
    # ========================================================

    if field in FIELD_RANGES:

        minimum, maximum = FIELD_RANGES[field]

        try:
            numeric_value = float(value)

        except (ValueError, TypeError):

            return {
                "valid": False,
                "message": (
                    f"Please enter a valid numeric value for {field}."
                )
            }

        if not minimum <= numeric_value <= maximum:

            return {
                "valid": False,
                "message": (
                    f"{field} ki value "
                    f"{minimum} se {maximum} ke beech honi chahiye."
                )
            }


    # ========================================================
    # TREATMENT STRING-CATEGORY FIELDS
    # ------------------------------------------------------
    # BUG FIX: these fields previously had no validation at all,
    # so an unrecognized value (e.g. a typo, or free text Gemini
    # couldn't map) would sail through and only fail much later
    # inside the model's preprocessing pipeline with a confusing
    # error.
    # ========================================================

    if field in TREATMENT_FIELD_OPTIONS:

        if value not in TREATMENT_FIELD_OPTIONS[field]:

            return {
                "valid": False,
                "message": (
                    f"Invalid value for {field}. "
                    f"Allowed values: {TREATMENT_FIELD_OPTIONS[field]}"
                )
            }


    # ========================================================
    # SMOKING HISTORY
    # ========================================================

    if field == "smoking_history":

        allowed = [
            "never",
            "No Info",
            "current",
            "former",
            "ever",
            "not current",
        ]

        if str(value).lower() not in [
            x.lower() for x in allowed
        ]:

            return {
                "valid": False,
                "message": (
                    f"Invalid value for smoking_history. "
                    f"Allowed values: {allowed}"
                )
            }


    # ========================================================
    # BMI CATEGORY
    # ========================================================

    if field == "bmi_category":

        allowed = [
            "Underweight",
            "Normal weight",
            "Overweight",
            "Obesity class 1",
            "Obesity class 2",
            "Obesity class 3",
        ]

        if value not in allowed:

            return {
                "valid": False,
                "message": (
                    f"Invalid value for bmi_category. "
                    f"Allowed values: {allowed}"
                )
            }


    # ========================================================
    # AGE GROUP
    # ========================================================

    if field == "age_group":

        allowed = [
            "Child",
            "Young",
            "Adult",
            "Middle_age",
            "Senior",
        ]

        if value not in allowed:

            return {
                "valid": False,
                "message": (
                    f"Invalid age group. Allowed values: {allowed}"
                )
            }


    # ========================================================
    # SUCCESS
    # ========================================================

    return {
        "valid": True,
        "message": "Valid input."
    }
