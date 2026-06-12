"""Custom exceptions for banking business rules."""


class BankingError(Exception):
    """Base exception for banking application errors."""


class AccountNotFoundError(BankingError):
    """Raised when an account number cannot be found."""


class InsufficientFundsError(BankingError):
    """Raised when withdrawal amount is greater than available balance."""


class InvalidAmountError(BankingError):
    """Raised when deposit or withdrawal amount is not positive."""
