from pydantic import BaseModel, Field
from typing import Literal


class HeartDiseaseInput(BaseModel):
    age: float = Field(..., ge=1, le=100)

    resting_bp_s: float = Field(..., ge=50, le=300)

    cholesterol: float = Field(..., ge=90, le=450)

    max_heart_rate: float = Field(..., ge=70, le=210)

    # BUG FIX: was "st_pepression" (typo). Renamed to "oldpeak" so this
    # matches the training feature name, the Gemini extraction schema
    # (chat_schema.HealthData.oldpeak) and questions.py/fields.py used by
    # the chatbot flow. The service layer no longer needs a special-case
    # rename for this field.
    oldpeak: float = Field(..., ge=-5, le=10)
        
    # BUG FIX: was Literal[1, 2, 3, 4]. validator.py's FIELD_RANGES /
    # chatbot flow used a 0-3 range for this field, causing chatbot-collected
    # values to fail this schema's validation (and vice versa). Standardized
    # on 1-4, since that is what the trained model's training data used to
    # look up (see FIELD_RANGES in validator.py, updated to match).
    chest_pain_type: Literal[1, 2, 3, 4]

    resting_ecg: int = Field(..., ge=0, le=2)

    st_slope: int = Field(..., ge=0, le=2)

    sex: int = Field(..., ge=0, le=1)

    fasting_blood_sugar: int = Field(..., ge=0, le=1)

    exercise_angina: int = Field(..., ge=0, le=1)
