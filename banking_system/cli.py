"""Command-line interface for the banking system."""
from __future__ import annotations

from banking_system.database import SessionLocal, init_db
from banking_system.exceptions import BankingError
from banking_system.services.banking_service import BankingService
from banking_system.utils.logger import setup_logger

logger = setup_logger()


def read_account_id() -> int:
    """Read account id from user input."""
    return int(input("Enter account number: ").strip())


def main() -> None:
    """Start the banking CLI application."""
    init_db()
    print("\nWelcome to SpringLake Bank - Banking Management System")

    with SessionLocal() as session:
        service = BankingService(session)
        while True:
            print("\n1. Open Account")
            print("2. Account Balance Details")
            print("3. Deposit Amount")
            print("4. Withdraw Amount")
            print("5. Close Account")
            print("6. Exit")
            choice = input("Choose an option: ").strip()

            try:
                if choice == "1":
                    first_name = input("First name: ").strip()
                    last_name = input("Last name: ").strip()
                    email = input("Email: ").strip()
                    phone = input("Phone (optional): ").strip() or None
                    address = input("Address (optional): ").strip() or None
                    account_type = input("Account type (CHECKING/SAVINGS): ").strip()
                    amount = service.parse_amount(input("Initial deposit: ").strip())
                    account_id = service.open_account(
                        first_name,
                        last_name,
                        email,
                        account_type,
                        amount,
                        phone,
                        address,
                    )
                    print(f"Account created successfully. Account number: {account_id}")
                elif choice == "2":
                    balance = service.get_balance(read_account_id())
                    print(f"Current balance: ${balance:.2f}")
                elif choice == "3":
                    account_id = read_account_id()
                    amount = service.parse_amount(input("Deposit amount: ").strip())
                    balance = service.deposit(account_id, amount)
                    print(f"Deposit complete. New balance: ${balance:.2f}")
                elif choice == "4":
                    account_id = read_account_id()
                    amount = service.parse_amount(input("Withdrawal amount: ").strip())
                    balance = service.withdraw(account_id, amount)
                    print(f"Withdrawal complete. New balance: ${balance:.2f}")
                elif choice == "5":
                    service.close_account(read_account_id())
                    print("Account closed successfully.")
                elif choice == "6":
                    print("Thank you for using SpringLake Bank.")
                    break
                else:
                    print("Invalid menu option. Please choose 1-6.")
            except (BankingError, ValueError) as exc:
                session.rollback()
                logger.warning("Handled application error: %s", exc)
                print(f"Error: {exc}")
            except Exception as exc:  # noqa: BLE001
                session.rollback()
                logger.exception("Unexpected error")
                print("Unexpected error occurred. Check logs/banking_system.log.")


if __name__ == "__main__":
    main()
