from typing import Any

from backend.services.diabetes_service import predict_diabetes
from backend.services.heart_dieses_service import predict_heart_dieses
from backend.services.treatment_service import predict_treatment

from src.chatbot.fields import get_age_group, get_bmi_category


def predict_health(condition: str, data: dict[str, Any]) -> dict[str, Any]:
    condition = condition.lower().strip()

    if condition == "diabetes":

        # ------------------------------------------------------
        # BUG FIX: age_group / bmi_category are marked as AUTO_FIELDS
        # in fields.py, meaning the chatbot never asks the user for
        # them and Gemini extraction never returns them either. That
        # meant predict_diabetes() always KeyError'd on the missing
        # "Age_group" / "BMI_category" columns whenever a prediction
        # came from the chatbot flow (or from /predict/health).
        # We now derive them here from age/bmi if not already present.
        # ------------------------------------------------------
        data = dict(data)

        if "age_group" not in data and data.get("age") is not None:
            data["age_group"] = get_age_group(data["age"])

        if "bmi_category" not in data and data.get("bmi") is not None:
            data["bmi_category"] = get_bmi_category(data["bmi"])

        result = predict_diabetes(data)

        return {
            "success": True,
            "condition": "diabetes",
            "prediction": result["prediction"],
            "probability": result["probability"],
            "probability_percent": result["probability_percent"],
            "threshold": result["threshold"],
            "threshold_percent": result["threshold_percent"],
            "risk_category": result["risk_category"],
        }

    if condition in {"heart", "heart_disease", "heart disease"}:
        result = predict_heart_dieses(data)

        return {
            "success": True,
            "condition": "heart",
            "prediction": result["prediction"],
            "probability": result["probability"],
            "probability_percent": result["probability_percent"],
            "threshold": result["threshold"],
            "threshold_percent": result["threshold_percent"],
            "risk_category": result["risk_category"],
        }

    if condition in {"treatment", "mental_health", "mental health"}:
        prediction = predict_treatment(data)

        return {
            "success": True,
            "condition": "treatment",
            "prediction": int(prediction),
            "treatment_needed": bool(prediction),
        }

    raise ValueError(
        f"Unsupported prediction condition: {condition}"
    )
