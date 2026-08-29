import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent

MODEL_DIR = BASE_DIR / "models"

model = joblib.load(
    MODEL_DIR / "Tretment_prediction.pkl"
)


top_countries = [
    'United States',
    'United Kingdom',
    'Canada',
    'Germany',
    'Netherlands',
    'Ireland',
    'Australia',
    'France',
    'India',
    'New Zealand'
]


def predict_treatment(data: dict):

    df = pd.DataFrame([data])

    # Country → Grouped_country
    df["Grouped_country"] = df["Country"].apply(
        lambda x: x if x in top_countries else "Other"
    )

    feature_column = [
        'Age',
        'Gender',
        'self_employed',
        'family_history',
        'work_interfere',
        'no_employees',
        'remote_work',
        'tech_company',
        'benefits',
        'care_options',
        'wellness_program',
        'seek_help',
        'anonymity',
        'leave',
        'mental_health_consequence',
        'phys_health_consequence',
        'coworkers',
        'supervisor',
        'mental_health_interview',
        'phys_health_interview',
        'mental_vs_physical',
        'obs_consequence',
        'Grouped_country'
    ]

    df = df[feature_column]

    prediction = model.predict(df)[0]

    return int(prediction)