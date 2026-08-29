import joblib
import pandas as pd
import xgboost as xgb
from pathlib import Path

# PATH

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_DIR = BASE_DIR / "models"


# Load processor

Heart_preprocessor = joblib.load(
    MODEL_DIR / "heart_preprocessor.pkl"
)


# XGBOOST MOdel

classifier = xgb.XGBClassifier()
classifier.load_model(
    MODEL_DIR / "heart_model.ubj"
)

# Load Threshold

with open(
    MODEL_DIR / "heart_threshold.txt",
    "r"
) as file:
    THRESHOLD = float(file.read())

# Prediction Function


def predict_heart_dieses(data: dict):
    df = pd.DataFrame([data])

    # BUG FIX: "st_pepression" -> "oldpeak" rename removed. The schema field
    # was renamed to "oldpeak" directly (see backend/schemas/heart_dieses.py),
    # and the chatbot flow already used "oldpeak" as its canonical name, so
    # this rename entry was both unnecessary and confusing.
    df.rename(
        columns={
            "resting_bp_s": "resting bp s",
            "max_heart_rate": "max heart rate",
            "chest_pain_type": "chest pain type",
            "resting_ecg": "resting ecg",
            "st_slope": "ST slope",
            "fasting_blood_sugar": "fasting blood sugar",
            "exercise_angina": "exercise angina",
        },
        inplace=True
    )

    # Exact training feature order
    Feature_columns = [
        'age',
        'resting bp s',
        'cholesterol',
        'max heart rate',
        'oldpeak',
        'chest pain type',
        'resting ecg',
        'ST slope',
        'sex',
        'fasting blood sugar',
        'exercise angina'
    ]
    df = df[Feature_columns]

    # Preprocessing
    X_process = Heart_preprocessor.transform(df)

    # probability

    heart_disease_probability = classifier.predict_proba(X_process)[0][1]

    # thershold

    HeartDieses_prediction = int(
        heart_disease_probability >= THRESHOLD
    )
    # risk Category
    if heart_disease_probability < 0.20:
        risk_category = "Low Risk"

    elif heart_disease_probability < 0.50:
        risk_category = "Moderate Risk"

    elif heart_disease_probability < 0.75:
        risk_category = "High Risk"

    else:
        risk_category = "Very High Risk"

    return {
        "prediction": int(HeartDieses_prediction),
        "probability": round(float(heart_disease_probability), 4),
        "probability_percent": round(
            float(heart_disease_probability) * 100, 2
        ),
        "threshold": THRESHOLD,
        "threshold_percent": round(float(THRESHOLD) * 100, 2),
        "risk_category": risk_category
    }
