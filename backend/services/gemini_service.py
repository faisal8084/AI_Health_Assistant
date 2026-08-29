import os
import json

from dotenv import load_dotenv
from google import genai

from backend.schemas.chat_schema import ChatbotExtraction


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# API KEY
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.6-flash"


# ============================================================
# NORMAL CHAT
# ============================================================

def ask_gemini(message: str) -> str:

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=message
    )

    return response.text


# ============================================================
# HEALTH DATA EXTRACTION
# ============================================================

def extract_health_data(
    message: str,
    condition: str | None = None,
    current_field: str | None = None
) -> ChatbotExtraction:

    context = f"""
Current assessment condition: {condition}
Current field/question being answered: {current_field}
"""

    prompt = f"""
You are an AI Health Assistant data extraction system.

{context}

Analyze ONLY the user's latest message.

The user may provide:

- complete information
- multiple health values
- or a short answer such as:
  Yes
  No
  Male
  Female
  55
  220
  140
  Never

IMPORTANT:

If current_field is provided, the user's short answer
must be mapped to that field.

User message:
{message}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "intent": "{condition if condition else 'unknown'}",

    "health_data": {{

        "gender": null,
        "age": null,
        "bmi": null,
        "hba1c_level": null,
        "blood_glucose_level": null,
        "smoking_history": null,
        "hypertension": null,
        "heart_disease": null,

        "sex": null,
        "chest_pain_type": null,
        "resting_bp_s": null,
        "cholesterol": null,
        "fasting_blood_sugar": null,
        "resting_ecg": null,
        "max_heart_rate": null,
        "exercise_angina": null,
        "oldpeak": null,
        "st_slope": null,

        "self_employed": null,
        "family_history": null,
        "work_interfere": null,
        "no_employees": null,
        "remote_work": null,
        "tech_company": null,
        "benefits": null,
        "care_options": null,
        "wellness_program": null,
        "seek_help": null,
        "anonymity": null,
        "leave": null,
        "mental_health_consequence": null,
        "phys_health_consequence": null,
        "coworkers": null,
        "supervisor": null,
        "mental_health_interview": null,
        "phys_health_interview": null,
        "mental_vs_physical": null,
        "obs_consequence": null,
        "country": null
    }},

    "missing_fields": []
}}

============================================================
DIABETES
============================================================

Fields:

gender
age
bmi
hba1c_level
blood_glucose_level
smoking_history
hypertension
heart_disease

For hypertension:

Yes = 1
No = 0

For heart_disease:

Yes = 1
No = 0


============================================================
HEART DISEASE
============================================================

Fields:

age
sex
chest_pain_type
resting_bp_s
cholesterol
fasting_blood_sugar
resting_ecg
max_heart_rate
exercise_angina
oldpeak
st_slope

For sex:

Male = 1
Female = 0

For fasting_blood_sugar:

Yes = 1
No = 0

For exercise_angina:

Yes = 1
No = 0


============================================================
TREATMENT
============================================================

Fields:

age
gender
self_employed
family_history
work_interfere
no_employees
remote_work
tech_company
benefits
care_options
wellness_program
seek_help
anonymity
leave
mental_health_consequence
phys_health_consequence
coworkers
supervisor
mental_health_interview
phys_health_interview
mental_vs_physical
obs_consequence
country


============================================================
IMPORTANT RULES
============================================================

1. Extract ONLY information explicitly present.

2. Never invent information.

3. If current_field is provided and the user gives
   a short answer, map that answer to current_field.

4. Do not map unrelated information.

5. Numeric values must be numbers.

6. Male/Female for heart disease must become
   sex = 1/0.

7. Yes/No for binary fields must become 1/0.

8. Return null when information is not provided.

9. Return JSON only.

10. Do not return markdown.

"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    raw_text = response.text.strip()

    # ========================================================
    # REMOVE MARKDOWN
    # ========================================================

    if raw_text.startswith("```"):

        raw_text = raw_text.replace(
            "```json",
            ""
        )

        raw_text = raw_text.replace(
            "```",
            ""
        )

        raw_text = raw_text.strip()

    # ========================================================
    # JSON
    # ========================================================

    data = json.loads(raw_text)

    # ========================================================
    # PYDANTIC VALIDATION
    # ========================================================

    validated_data = ChatbotExtraction.model_validate(
        data
    )

    return validated_data