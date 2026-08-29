# ============================================================
# QUESTION DEFINITIONS
# ============================================================

QUESTIONS = {
    "diabetes": [
        {
            "field": "gender",
            "question": "Aapka gender kya hai? (Male/Female/Other)"
        },
        {
            "field": "age",
            "question": "Aapki age kya hai?"
        },
        {
            "field": "bmi",
            "question": "Aapka BMI kya hai?"
        },
        {
            "field": "smoking_history",
            "question": (
                "Aapki smoking history kya hai? "
                "(never/No Info/current/former/ever/not current)"
            )
        },
        {
            "field": "HbA1c_level",
            "question": "Aapka HbA1c level kya hai?"
        },
        {
            "field": "blood_glucose_level",
            "question": "Aapka blood glucose level kya hai?"
        },
        {
            "field": "hypertension",
            "question": "Kya aapko hypertension hai? (Yes/No)"
        },
        {
            "field": "heart_disease",
            "question": "Kya aapko heart disease hai? (Yes/No)"
        },
    ],

    "heart": [
        {
            "field": "age",
            "question": "Aapki age kya hai?"
        },
        {
            "field": "sex",
            "question": "Aapka sex kya hai? (Male/Female)"
        },
        {
            "field": "chest_pain_type",
            "question": "Chest pain type kya hai? (1/2/3/4)"
        },
        {
            "field": "resting_bp_s",
            "question": "Aapka resting blood pressure (systolic) kya hai?"
        },
        {
            "field": "cholesterol",
            "question": "Aapka cholesterol level kya hai?"
        },
        {
            "field": "fasting_blood_sugar",
            "question": "Kya fasting blood sugar 120 mg/dl se zyada hai? (Yes/No)"
        },
        {
            "field": "resting_ecg",
            "question": "Aapka resting ECG result kya hai? (0/1/2)"
        },
        {
            "field": "max_heart_rate",
            "question": "Aapka maximum heart rate kya hai?"
        },
        {
            "field": "exercise_angina",
            "question": "Exercise ke dauran angina hota hai? (Yes/No)"
        },
        {
            "field": "oldpeak",
            "question": "Aapka oldpeak value kya hai?"
        },
        {
            "field": "st_slope",
            "question": "Aapka ST slope kya hai? (0/1/2)"
        },
    ],

    "treatment": [
        {"field": "age", "question": "Aapki age kya hai?"},
        {"field": "gender", "question": "Aapka gender kya hai? (Male/Female/Other)"},
        {"field": "self_employed", "question": "Kya aap self-employed hain? (Yes/No)"},
        {"field": "family_history", "question": "Kya family mein mental health history hai? (Yes/No)"},
        {
            "field": "work_interfere",
            "question": "Mental health aapke work ko kitna affect karti hai? (Often/Rarely/Never/Sometimes/Unknown)"
        },
        {
            "field": "no_employees",
            "question": "Aapki company mein kitne employees hain? (1-5/6-25/26-100/100-500/500-1000/More than 1000)"
        },
        {"field": "remote_work", "question": "Kya aap remote work karte hain? (Yes/No)"},
        {"field": "tech_company", "question": "Kya aap tech company mein kaam karte hain? (Yes/No)"},
        {"field": "benefits", "question": "Kya workplace mental health benefits provide karta hai? (Yes/No/Don't know)"},
        {"field": "care_options", "question": "Kya aapko mental health care options available hain? (Yes/No/Not sure)"},
        {"field": "wellness_program", "question": "Kya workplace wellness program provide karta hai? (Yes/No/Don't know)"},
        {"field": "seek_help", "question": "Kya aap mental health ke liye help seek kar sakte hain? (Yes/No/Don't know)"},
        {"field": "anonymity", "question": "Kya treatment lene par anonymity maintain ho sakti hai? (Yes/No/Don't know)"},
        {
            "field": "leave",
            "question": "Mental health ke liye leave lena kitna easy hai? (Very easy/Somewhat easy/Don't know/Somewhat difficult/Very difficult)"
        },
        {"field": "mental_health_consequence", "question": "Mental health issue ka work par consequence kya ho sakta hai? (Yes/No/Maybe)"},
        {"field": "phys_health_consequence", "question": "Physical health issue ka work par consequence kya ho sakta hai? (Yes/No/Maybe)"},
        {"field": "coworkers", "question": "Kya aap coworkers se mental health discuss kar sakte hain? (Yes/No/Some of them)"},
        {"field": "supervisor", "question": "Kya aap supervisor se mental health discuss kar sakte hain? (Yes/No/Some of them)"},
        {"field": "mental_health_interview", "question": "Kya mental health ke baare mein interview mein question hona acceptable hai? (Yes/No/Maybe)"},
        {"field": "phys_health_interview", "question": "Kya physical health ke baare mein interview mein question hona acceptable hai? (Yes/No/Maybe)"},
        {"field": "mental_vs_physical", "question": "Kya employer mental health ko physical health jitna seriously leta hai? (Yes/No/Don't know)"},
        {"field": "obs_consequence", "question": "Kya mental health issue ne work par negative consequence diya hai? (Yes/No)"},
        {"field": "country", "question": "Aap kis country mein rehte hain?"},
    ],
}


def next_question(condition: str, data: dict, canonicalize=None):
    """Return the next unanswered question for `condition`.

    BUG FIX: this file's field names (e.g. "chest_pain_type", "age"
    for treatment) don't always match the canonical training-column
    names the rest of the app stores answers under (e.g. heart's
    canonical name is "chest pain type", treatment's is "Age").
    Previously this function checked `item["field"] not in data`
    using its own raw name, so once chatbot_engine.py started storing
    answers under the canonical name (see BUG FIX there), an answered
    question would never be recognized as answered - the same
    question would be asked forever.

    `canonicalize` is an optional callable (chatbot_engine.py passes
    ChatbotEngine.get_canonical_field) used to translate this file's
    field name into the canonical one before checking `data`.
    """

    if condition not in QUESTIONS:
        return None

    for item in QUESTIONS[condition]:

        field = item["field"]

        check_field = canonicalize(field) if canonicalize else field

        if check_field not in data:
            return item

    return None
