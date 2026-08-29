"""
============================================================
AUTH DEPENDENCY
Protects routes: verifies the JWT bearer token and loads the
corresponding active user from PostgreSQL.
============================================================
"""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.services.auth_service import decode_access_token

# auto_error=False lets us raise our own consistent 401 JSON shape
# instead of FastAPI's default "Not authenticated" text response.
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        user_id = decode_access_token(credentials.credentials)
    except JWTError:
        raise unauthorized

    try:
        user_uuid = uuid.UUID(user_id)
    except (ValueError, TypeError):
        raise unauthorized

    user = db.query(User).filter(User.id == user_uuid).first()

    if user is None or not user.is_active:
        raise unauthorized

    return user
