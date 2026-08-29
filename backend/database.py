"""
============================================================
DATABASE SETUP (PostgreSQL via SQLAlchemy)
============================================================
Reads DATABASE_URL from the environment (.env). Never hard-code
credentials here.

Example .env value:
    DATABASE_URL=postgresql://username:password@localhost:5432/ai_health_assistant
============================================================
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Copy .env.example to .env and set it."
    )

# pool_pre_ping avoids stale-connection errors after idle periods.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Create tables that don't exist yet.
    Does NOT touch or drop any existing tables/data — safe to call
    on every startup. For real schema migrations, use Alembic instead.
    """
    # Import models here so they're registered on Base before create_all.
    from backend.models.user import User  # noqa: F401

    Base.metadata.create_all(bind=engine)
