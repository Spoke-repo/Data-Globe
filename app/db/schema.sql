CREATE TABLE IF NOT EXISTS customers (
    id     SERIAL PRIMARY KEY,
    name   TEXT NOT NULL,
    region TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    customer_id INTEGER REFERENCES customers(id),
    amount      NUMERIC(12, 2) NOT NULL
);
