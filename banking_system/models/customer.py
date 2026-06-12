"""Customer ORM model."""
from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from banking_system.models.base import Base


class Customer(Base):
    """Represents a bank customer."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(25))
    address: Mapped[str | None] = mapped_column(String(255))

    accounts: Mapped[list["BankAccount"]] = relationship(back_populates="customer")
