"""Banking service layer containing application use cases."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation

from sqlalchemy.orm import Session

from banking_system.exceptions import AccountNotFoundError, InvalidAmountError
from banking_system.repositories.banking_repository import BankingRepository


class BankingService:
    """Coordinates repository calls and account business rules."""

    def __init__(self, session: Session) -> None:
        self.repository = BankingRepository(session)
        self.session = session

    @staticmethod
    def parse_amount(value: str) -> Decimal:
        """Convert user input to a Decimal amount."""
        try:
            amount = Decimal(value)
        except InvalidOperation as exc:
            raise InvalidAmountError("Please enter a valid numeric amount.") from exc
        if amount <= 0:
            raise InvalidAmountError("Amount must be greater than zero.")
        return amount

    def open_account(
        self,
        first_name: str,
        last_name: str,
        email: str,
        account_type: str,
        initial_deposit: Decimal,
        phone: str | None = None,
        address: str | None = None,
    ) -> int:
        """Create a new customer and bank account, then return account id."""
        if account_type.upper() not in {"CHECKING", "SAVINGS"}:
            raise ValueError("Account type must be CHECKING or SAVINGS.")
        customer = self.repository.create_customer(first_name, last_name, email, phone, address)
        account = self.repository.create_account(customer.id, account_type, initial_deposit)
        self.session.commit()
        return account.id

    def get_balance(self, account_id: int) -> Decimal:
        """Return current account balance."""
        account = self.repository.get_account(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} was not found.")
        return Decimal(account.balance)

    def deposit(self, account_id: int, amount: Decimal) -> Decimal:
        """Deposit money into an account."""
        account = self.repository.get_account(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} was not found.")
        new_balance = account.deposit(amount)
        self.session.commit()
        return new_balance

    def withdraw(self, account_id: int, amount: Decimal) -> Decimal:
        """Withdraw money from an account."""
        account = self.repository.get_account(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} was not found.")
        new_balance = account.withdraw(amount)
        self.session.commit()
        return new_balance

    def close_account(self, account_id: int) -> None:
        """Close an existing account."""
        account = self.repository.get_account(account_id)
        if not account:
            raise AccountNotFoundError(f"Account {account_id} was not found.")
        account.close()
        self.session.commit()
