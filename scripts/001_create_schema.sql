-- Optional SQL script. The Python app also creates these tables automatically
-- through SQLAlchemy Base.metadata.create_all() before the CLI starts.

CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(25),
    address VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    account_type VARCHAR(20) NOT NULL,
    balance NUMERIC(12, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    overdraft_limit NUMERIC(12, 2) DEFAULT 0,
    interest_rate NUMERIC(5, 4) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS loans (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    loan_type VARCHAR(30) NOT NULL,
    principal NUMERIC(12, 2) NOT NULL,
    interest_rate NUMERIC(5, 4) NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS credit_cards (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    card_number_last4 VARCHAR(4) NOT NULL,
    credit_limit NUMERIC(12, 2) NOT NULL,
    current_balance NUMERIC(12, 2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'ACTIVE'
);
