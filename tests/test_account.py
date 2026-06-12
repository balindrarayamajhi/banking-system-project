"""Simple unit tests for account behavior."""
from decimal import Decimal

import pytest

from banking_system.exceptions import InsufficientFundsError
from banking_system.models.account import CheckingAccount


def test_deposit_increases_balance():
    account = CheckingAccount(customer_id=1, balance=Decimal("100.00"), overdraft_limit=100)
    assert account.deposit(Decimal("25.00")) == Decimal("125.00")


def test_withdraw_checks_available_balance():
    account = CheckingAccount(customer_id=1, balance=Decimal("50.00"), overdraft_limit=0)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(Decimal("75.00"))
