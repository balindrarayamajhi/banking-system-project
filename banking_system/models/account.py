"""Bank account ORM models and business behavior."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from banking_system.exceptions import InsufficientFundsError, InvalidAmountError
from banking_system.models.base import Base


class BankAccount(Base):
    """Base account class for common checking and savings behavior."""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    account_type: Mapped[str] = mapped_column(String(20), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE")
    opened_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    overdraft_limit: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    interest_rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), default=0)

    customer: Mapped["Customer"] = relationship(back_populates="accounts")

    __mapper_args__ = {
        "polymorphic_on": account_type,
        "polymorphic_identity": "BASE",
    }

    @property
    def available_balance(self) -> Decimal:
        """Return the balance available for withdrawal."""
        return Decimal(self.balance) + Decimal(self.overdraft_limit)

    def deposit(self, amount: Decimal) -> Decimal:
        """Deposit a positive amount and return the new balance."""
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than zero.")
        self.balance = Decimal(self.balance) + amount
        return Decimal(self.balance)

    def withdraw(self, amount: Decimal) -> Decimal:
        """Withdraw a positive amount when sufficient funds are available."""
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than zero.")
        if amount > self.available_balance:
            raise InsufficientFundsError("Insufficient funds for this withdrawal.")
        self.balance = Decimal(self.balance) - amount
        return Decimal(self.balance)

    def close(self) -> None:
        """Close the account."""
        self.status = "CLOSED"


class CheckingAccount(BankAccount):
    """Checking account with a small overdraft limit."""

    __mapper_args__ = {"polymorphic_identity": "CHECKING"}


class SavingsAccount(BankAccount):
    """Savings account that can earn interest."""

    __mapper_args__ = {"polymorphic_identity": "SAVINGS"}
