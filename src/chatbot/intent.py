# ============================================================
# BUG FIX: this file did not exist at all in the uploaded project,
# even though chatbot_engine.py does:
#
#     from src.chatbot.intent import detect_intent
#
# That import would fail immediately on startup (ModuleNotFoundError),
# crashing the whole app before a single request could be served.
#
# This module provides a simple keyword-based fallback intent
# detector, used only when Gemini extraction fails or returns
# "unknown" (see STEP 2 in chatbot_engine.process_message).
# ============================================================

DIABETES_KEYWORDS = [
    "diabetes",
    "sugar",
    "blood sugar",
    "glucose",
    "madhumeh",
    "sugar ki bimari",
    "hba1c",
]

HEART_KEYWORDS = [
    "heart",
    "cardiac",
    "cardio",
    "chest pain",
    "dil",
    "dil ki bimari",
    "cholesterol",
]

TREATMENT_KEYWORDS = [
    "mental health",
    "mental",
    "depression",
    "anxiety",
    "stress",
    "tension",
    "therapy",
    "counseling",
    "counselling",
    "workplace",
    "treatment",
]


def detect_intent(message: str) -> str:
    """Very small keyword-based intent classifier used as a fallback
    when Gemini extraction is unavailable or returns 'unknown'."""

    if not message:
        return "unknown"

    text = message.lower()

    if any(keyword in text for keyword in DIABETES_KEYWORDS):
        return "diabetes"

    if any(keyword in text for keyword in HEART_KEYWORDS):
        return "heart"

    if any(keyword in text for keyword in TREATMENT_KEYWORDS):
        return "treatment"

    return "unknown"
