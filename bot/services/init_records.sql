CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT,
    name VARCHAR(24),
    surname VARCHAR(24),
    nickname VARCHAR(24),
    is_subscribed BOOLEAN,
    date TIMESTAMP
);
