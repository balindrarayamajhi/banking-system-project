"""Repository layer for database operations."""
from __future__ import annotations

from sqlalchemy.orm import Session

from banking_system.models import BankAccount, CheckingAccount, Customer, SavingsAccount


class BankingRepository:
    """Encapsulates SQLAlchemy persistence operations."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_customer(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
        address: str | None = None,
    ) -> Customer:
        """Create and save a customer."""
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
        )
        self.session.add(customer)
        self.session.flush()
        return customer

    def create_account(
        self,
        customer_id: int,
        account_type: str,
        initial_deposit,
    ) -> BankAccount:
        """Create and save a checking or savings account."""
        if account_type.upper() == "CHECKING":
            account = CheckingAccount(
                customer_id=customer_id,
                balance=initial_deposit,
                overdraft_limit=100,
                interest_rate=0,
            )
        else:
            account = SavingsAccount(
                customer_id=customer_id,
                balance=initial_deposit,
                overdraft_limit=0,
                interest_rate=0.015,
            )
        self.session.add(account)
        self.session.flush()
        return account

    def get_account(self, account_id: int) -> BankAccount | None:
        """Return account by id."""
        return self.session.get(BankAccount, account_id)
