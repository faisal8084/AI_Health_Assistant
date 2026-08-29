from fastapi import FastAPI, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.schemas.diabetes import DiabetesInput
from backend.services.diabetes_service import predict_diabetes

from backend.schemas.heart_dieses import HeartDiseaseInput
from backend.services.heart_dieses_service import predict_heart_dieses

from backend.schemas.treatment import treatmentInput
from backend.services.treatment_service import predict_treatment

from backend.schemas.health_schema import HealthPredictionRequest
from src.prediction_engine import predict_health

from backend.services.chat_service import (
    process_chat,
    reset_chat
)

from backend.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    ResetRequest,
    ResetResponse
)

# NEW: authentication
from backend.database import init_db
from backend.dependencies import get_current_user
from backend.models.user import User
from backend.routers.auth import router as auth_router


app = FastAPI(
    title="AI Health Assistant API",
    description="AI-based health risk prediction API",
    version="1.0.0"
)
app.include_router(auth_router)

# --------------------------------------------------------------
# STARTUP
# NEW: create the `users` table if it doesn't exist yet. This never
# touches existing tables/data and is safe to run on every boot.
# For real schema changes going forward, use Alembic migrations.
# --------------------------------------------------------------

@app.on_event("startup")
def on_startup():
    init_db()


# NEW: authentication routes (/auth/register, /auth/login, /auth/me, /auth/logout)
app.include_router(auth_router)


# --------------------------------------------------------------
# CORS
# NEW: required so the frontend (served from a different
# origin/port, e.g. http://localhost:5500 or a static file server)
# can call this API from the browser. Configurable via the
# ALLOWED_ORIGINS env var (comma-separated). Defaults to common
# local dev origins plus "*" so the bundled frontend works
# out of the box; tighten this for production deployments.
# --------------------------------------------------------------

_allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")

_allowed_origins = (
    ["*"]
    if _allowed_origins_env.strip() == "*"
    else [o.strip() for o in _allowed_origins_env.split(",") if o.strip()]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "Something went wrong. Please try again."
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "details": exc.errors()
        }
    )


@app.get("/")
def home():

    return {
        "message": "AI Health Assistant API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.post("/predict/diabetes")
def diabetes_prediction(
    data: DiabetesInput,
    current_user: User = Depends(get_current_user)
):

    result = predict_diabetes(
        data.model_dump()
    )

    return {
        "success": True,
        "disease": "Diabetes",
        "result": result
    }


@app.post("/predict/heartDieses")
def heartDieses_prediction(
    data: HeartDiseaseInput,
    current_user: User = Depends(get_current_user)
):
    heart_result = predict_heart_dieses(
        data.model_dump()
    )

    # BUG FIX: was "succes"/"diease" (typos) - fixed to "success"/"disease"
    # for consistency with every other endpoint's response shape.
    return {
        "success": True,
        "disease": "Heart_dieses",
        "result": heart_result
    }


@app.post("/predict/treatment")
def treatment_prediction(
    data: treatmentInput,
    current_user: User = Depends(get_current_user)
):
    treatment_result = predict_treatment(
        data.model_dump()
    )

    # BUG FIX: was "succes" (typo) - fixed to "success".
    return {
        "success": True,
        "treatment": "treatment",
        "result": treatment_result
    }


@app.post("/predict/health")
def health_prediction(
    request: HealthPredictionRequest,
    current_user: User = Depends(get_current_user)
):

    # BUG FIX: predict_health() raises ValueError for an unsupported
    # condition, but this endpoint had no try/except, so it fell
    # through to the generic 500 exception handler with a useless
    # "Internal server error" message instead of a clear 400.
    try:

        result = predict_health(
            request.condition,
            request.data
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    try:

        result = process_chat(
            data.session_id,
            data.message
        )

        return {
            "success": True,
            "session_id": data.session_id,
            "result": result
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Prediction service temporarily unavailable."
        )


@app.post(
    "/chat/reset",
    response_model=ResetResponse
)
def reset_chat_session(
    data: ResetRequest,
    current_user: User = Depends(get_current_user)
):

    return reset_chat(
        data.session_id
    )
