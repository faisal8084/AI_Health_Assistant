from typing import Any, Optional, Literal
from pydantic import BaseModel, Field


# ============================================================
# CHAT REQUEST / RESPONSE
# ============================================================

class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        min_length=1,
        description="Unique conversation session ID"
    )

    message: str = Field(
        ...,
        min_length=1,
        description="User message"
    )


class ChatResponse(BaseModel):
    success: bool
    session_id: str
    result: dict[str, Any]


class ResetRequest(BaseModel):
    session_id: str = Field(
        ...,
        min_length=1,
        description="Session ID to reset"
    )


class ResetResponse(BaseModel):
    success: bool
    message: str


# ============================================================
# HEALTH DATA
# ============================================================

class HealthData(BaseModel):

    # ------------------------
    # DIABETES
    # ------------------------

    gender: Optional[
        Literal["Female", "Male", "Other"]
    ] = None

    age: Optional[float] = Field(
        default=None,
        ge=0,
        le=120
    )

    bmi: Optional[float] = Field(
        default=None,
        ge=5,
        le=100
    )

    hba1c_level: Optional[float] = Field(
        default=None,
        ge=0,
        le=20
    )

    blood_glucose_level: Optional[float] = Field(
        default=None,
        ge=0,
        le=1000
    )

    smoking_history: Optional[str] = None

    hypertension: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    heart_disease: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    # ------------------------
    # HEART
    # ------------------------

    sex: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    chest_pain_type: Optional[int] = None

    resting_bp_s: Optional[float] = None

    cholesterol: Optional[float] = None

    fasting_blood_sugar: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    resting_ecg: Optional[int] = None

    max_heart_rate: Optional[float] = None

    exercise_angina: Optional[int] = Field(
        default=None,
        ge=0,
        le=1
    )

    oldpeak: Optional[float] = None

    st_slope: Optional[int] = None

    # ------------------------
    # TREATMENT
    # ------------------------

    self_employed: Optional[str] = None
    family_history: Optional[str] = None
    work_interfere: Optional[str] = None
    no_employees: Optional[str] = None
    remote_work: Optional[str] = None
    tech_company: Optional[str] = None
    benefits: Optional[str] = None
    care_options: Optional[str] = None
    wellness_program: Optional[str] = None
    seek_help: Optional[str] = None
    anonymity: Optional[str] = None
    leave: Optional[str] = None

    mental_health_consequence: Optional[str] = None
    phys_health_consequence: Optional[str] = None

    coworkers: Optional[str] = None
    supervisor: Optional[str] = None

    mental_health_interview: Optional[str] = None
    phys_health_interview: Optional[str] = None

    mental_vs_physical: Optional[str] = None
    obs_consequence: Optional[str] = None

    country: Optional[str] = None


# ============================================================
# GEMINI EXTRACTION RESPONSE
# ============================================================

class ChatbotExtraction(BaseModel):

    intent: Literal[
        "diabetes",
        "heart_disease",
        "treatment",
        "general_health",
        "unknown"
    ] = "unknown"

    health_data: HealthData = Field(
        default_factory=HealthData
    )

    missing_fields: list[str] = Field(
        default_factory=list
    )