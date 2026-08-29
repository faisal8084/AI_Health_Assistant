import joblib
import xgboost as xgb
import pandas as pd

from pathlib import Path


# Paths

BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_DIR = BASE_DIR / "models"


# Load Preprocessor

preprocessor = joblib.load(
    MODEL_DIR / "diabetes_preprocessor.pkl"
)


# Load XGBoost Model

classifier = xgb.XGBClassifier()

classifier.load_model(
    MODEL_DIR / "diabetes_xgboost.ubj"
)


# --------------------------------------------------
# Load Threshold
# --------------------------------------------------

with open(
    MODEL_DIR / "diabetes_threshold.txt",
    "r"
) as file:

    THRESHOLD = float(file.read())


# --------------------------------------------------
# Prediction Function
# --------------------------------------------------

def predict_diabetes(data: dict):

    df = pd.DataFrame([data])

    # Convert API field name to training column name
    df.rename(
        columns={
            "age_group": "Age_group",
            "bmi_category": "BMI_category"
        },
        inplace=True
    )

    # Exact training feature order
    feature_columns = [
        "gender",
        "Age_group",
        "smoking_history",
        "BMI_category",
        "age",
        "bmi",
        "HbA1c_level",
        "blood_glucose_level",
        "hypertension",
        "heart_disease"
    ]

    df = df[feature_columns]

    # Preprocessing
    X_processed = preprocessor.transform(df)

    # Probability
    probability = classifier.predict_proba(
        X_processed
    )[0][1]

    # Threshold-based prediction
    prediction = int(
        probability >= THRESHOLD
    )

    # Risk category
    if probability < 0.25:
        risk_category = "Low Risk"

    elif probability < 0.50:
        risk_category = "Moderate Risk"

    elif probability < 0.75:
        risk_category = "High Risk"

    else:
        risk_category = "Very High Risk"

    return {
        "prediction": prediction,
        "probability": round(float(probability), 6),
        "probability_percent": round(float(probability) * 100, 2),
        "threshold": THRESHOLD,
        "threshold_percent": THRESHOLD * 100,
        "risk_category": risk_category
    }