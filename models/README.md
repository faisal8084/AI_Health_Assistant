# models/

Yeh folder **empty** hai — aapko apni trained model files yahin daalni hongi
(yeh files upload nahi hui thi, isliye include nahi ki gayi hain).

Required filenames (services in bilkul yehi naam expect karte hain):

| File | Used by |
|---|---|
| `diabetes_preprocessor.pkl` | `backend/services/diabetes_service.py` |
| `diabetes_xgboost.ubj` | `backend/services/diabetes_service.py` |
| `diabetes_threshold.txt` | `backend/services/diabetes_service.py` (single float value) |
| `heart_preprocessor.pkl` | `backend/services/heart_dieses_service.py` |
| `heart_model.ubj` | `backend/services/heart_dieses_service.py` |
| `heart_threshold.txt` | `backend/services/heart_dieses_service.py` (single float value) |
| `Tretment_prediction.pkl` | `backend/services/treatment_service.py` (naam mein typo hai, but code isi naam se load karta hai — file ka naam waisa hi rakhein, ya renaming chahiye to `treatment_service.py` mein bhi update kar dein) |

Without these files the app will still start, but any prediction request
(`/predict/diabetes`, `/predict/heartDieses`, `/predict/treatment`,
`/predict/health`, `/chat`) will fail at import time with a
`FileNotFoundError`.
