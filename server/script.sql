CREATE TABLE kash_users (
    id SERIAL PRIMARY KEY,
    etTag INTEGER,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(15) UNIQUE,
    birthday TIMESTAMP,
    password TEXT NOT NULL, -- Store pre-hashed password
    profile_pic_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP
);

-- Table: kash_user_wallet
CREATE TABLE kash_user_wallet (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    wallet_name VARCHAR(255) NOT NULL,
    balance NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    wallet_type VARCHAR(50) NOT NULL, -- e.g., 'cash', 'bank', 'crypto'
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: kash_expense_user
CREATE TABLE kash_expense_user (
    id SERIAL PRIMARY KEY,
    etTag INTEGER,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    wallet_id INTEGER REFERENCES kash_user_wallet(id) ON DELETE CASCADE,
    cat_id INTEGER,
    expense_name VARCHAR(255) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50), -- e.g., 'credit card', 'cash'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: kash_income_user
CREATE TABLE kash_income_user (
    id SERIAL PRIMARY KEY,
    etTag INTEGER,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    wallet_id INTEGER REFERENCES kash_user_wallet(id) ON DELETE CASCADE,
    cat_id INTEGER, -- Assuming a separate table for categories
    income_name VARCHAR(255) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(255), -- e.g., 'salary', 'investment'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: kash_payment_history
CREATE TABLE kash_payment_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    expense_id INTEGER REFERENCES kash_expense_user(id) ON DELETE CASCADE,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_amount NUMERIC(12, 2) NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'paid', -- e.g., 'paid', 'due'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: kash_budget
CREATE TABLE kash_budget (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    cat_id INTEGER,
    wallet_id INTEGER REFERENCES kash_user_wallet(id) ON DELETE CASCADE,
    budget_amount NUMERIC(12, 2) NOT NULL,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: kash_notifications
CREATE TABLE kash_notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- e.g., 'payment reminder', 'budget exceeded'
    message TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'unread', -- e.g., 'read', 'unread'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: kash_savings
CREATE TABLE kash_savings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES kash_users(id) ON DELETE CASCADE,
    goal_name VARCHAR(255) NOT NULL,
    target_amount NUMERIC(12, 2) NOT NULL,
    current_amount NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mock Data: Insert Users with Hashed Passwords
-- Insert Mock Data into kash_users (passwords pre-hashed in Python)
INSERT INTO kash_users (etTag, username, email, phone_number, birthday, password, profile_pic_url)
VALUES
    (1, 'john_doe', 'john@example.com', '1234567890', '1990-01-01', '$2b$12$ExampleHashJohnDoe123456', 'https://example.com/john.png'),
    (2, 'jane_doe', 'jane@example.com', '0987654321', '1992-02-02', '$2b$12$ExampleHashJaneDoeSecure', 'https://example.com/jane.png'),
    (3, 'alice_smith', 'alice@example.com', '5678901234', '1995-03-03', '$2b$12$ExampleHashAliceSmithPwd', 'https://example.com/alice.png');

-- Insert Mock Data into kash_user_wallet
INSERT INTO kash_user_wallet (user_id, wallet_name, balance, wallet_type, currency)
VALUES
    (1, 'Main Wallet', 1000.00, 'cash', 'USD'),
    (2, 'Savings Account', 2500.00, 'bank', 'USD'),
    (3, 'Crypto Wallet', 500.00, 'crypto', 'USD');