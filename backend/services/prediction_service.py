from typing import Any

from .diabetes_service import predict_diabetes
from .heart_dieses_service import predict_heart_dieses
from .treatment_service import predict_treatment


# ============================================================
# DIABETES
# ============================================================

def run_diabetes_prediction(data: dict[str, Any]) -> dict[str, Any]:
    """
    Run diabetes prediction using diabetes_service.
    """
    return predict_diabetes(data)


# ============================================================
# HEART DISEASE
# ============================================================

def run_heart_prediction(data: dict[str, Any]) -> dict[str, Any]:
    """
    Run heart disease prediction using heart_disease_service.
    """
    return predict_heart_dieses(data)


# ============================================================
# TREATMENT
# ============================================================

def run_treatment_prediction(data: dict[str, Any]) -> dict[str, Any]:
    """
    Run treatment prediction using treatment_service.
    """

    prediction = predict_treatment(data)

    return {
        "prediction": prediction,
        "treatment_needed": bool(prediction)
    }


# ============================================================
# GENERIC PREDICTION
# ============================================================

def run_prediction(
    intent: str,
    data: dict[str, Any]
) -> dict[str, Any]:

    intent = intent.lower().strip()

    if intent == "diabetes":
        return run_diabetes_prediction(data)

    elif intent in ["heart", "heart_disease", "heart disease"]:
        return run_heart_prediction(data)

    elif intent in ["treatment", "mental_health", "mental health"]:
        return run_treatment_prediction(data)

    else:
        raise ValueError(
            f"Unsupported prediction intent: {intent}"
        )