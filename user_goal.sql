CREATE TABLE user_goals (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    goal VARCHAR(255) NOT NULL,
    weightage INTEGER CHECK (weightage >= 0 AND weightage <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
