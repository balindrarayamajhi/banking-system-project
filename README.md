# Banking System Project

This is a simple command-line banking system built with Python OOP, SQLAlchemy ORM, and PostgreSQL. The project follows a package-based structure inspired by *The Hitchhiker's Guide to Python* project-structure guidance.

## Features

- Open a checking or savings account
- View account balance
- Deposit money
- Withdraw money with balance validation
- Close an account
- Persist data in PostgreSQL using SQLAlchemy ORM
- Create database tables automatically before the program starts
- Optional SQL schema script included in `scripts/001_create_schema.sql`
- Console logging and file logging in `logs/banking_system.log`
- Exception handling for invalid amounts, missing accounts, and insufficient funds

## Project Structure

```text
banking-system-project/
├── banking_system/
│   ├── cli.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   ├── models/
│   ├── repositories/
│   ├── services/
│   └── utils/
├── docs/
│   └── banking class diagram.png

├── logs/
├── scripts/
│   └── 001_create_schema.sql
├── tests/
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- Docker Desktop
- PostgreSQL runs locally through Docker Compose

## Setup Steps

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```



### 2. Install dependencies

```bash
pip install -r requirements.txt
```


### 3. Start PostgreSQL locally

```bash
docker compose up -d
```

Check that the container is running:

```bash
docker ps
```

### 4. Run the application

```bash
python main.py
```

When the program starts, it calls `init_db()` and creates the required tables automatically using SQLAlchemy ORM.

## Optional: Run the SQL Script Manually

The app creates tables automatically, but you can also run the SQL script manually:

```bash
docker exec -i banking_postgres psql -U banking_user -d banking_db < scripts/001_create_schema.sql
```

## Menu Options

1. **Open Account** - Create a customer and checking/savings account
2. **Account Balance Details** - View account balance
3. **Deposit Amount** - Add funds to an account
4. **Withdraw Amount** - Withdraw funds with validation
5. **Close Account** - Mark account as closed
6. **Exit** - Quit the program

## UML Diagram

See `docs/uml.md` for the Mermaid UML diagram.

## Design Notes

The system separates responsibilities into layers:

- `models`: SQLAlchemy ORM classes and account business behavior
- `repositories`: database persistence operations
- `services`: application use cases and validation
- `cli`: command-line user interface
- `utils`: logging setup

## Link for class digram 
https://lucid.app/lucidchart/68760757-810f-4c3b-9fbc-d3329e6af6df/edit?page=0_0#