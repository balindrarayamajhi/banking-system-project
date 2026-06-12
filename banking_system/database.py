"""Database engine, session factory, and schema initialization helpers."""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from banking_system.config import DATABASE_URL

from banking_system.models.base import Base

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """Create all database tables before the CLI program starts."""
    # from banking_system.models import account, customer, employee, loan, credit_card  # noqa: F401

    Base.metadata.create_all(bind=engine)
