from typing import Literal

from pydantic import BaseModel, Field


class DiabetesInput(BaseModel):

    gender: Literal["Female", "Male", "Other"]

    age_group: Literal[
        "Child",
        "Young",
        "Adult",
        "Middle_age",
        "Senior"
    ]

    smoking_history: Literal[
        "never",
        "No Info",
        "current",
        "former",
        "ever",
        "not current"
    ]

    bmi_category: Literal[
        "Underweight",
        "Normal weight",
        "Overweight",
        "Obesity class 1",
        "Obesity class 2",
        "Obesity class 3"
    ]

    age: float = Field(..., ge=0, le=120)

    bmi: float = Field(..., gt=0, le=100)

    HbA1c_level: float = Field(..., ge=0, le=20)

    blood_glucose_level: float = Field(..., ge=0, le=1000)

    hypertension: int = Field(..., ge=0, le=1)

    heart_disease: int = Field(..., ge=0, le=1)