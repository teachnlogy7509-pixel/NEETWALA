
CREATE TABLE IF NOT EXISTS progress(
    user_id INTEGER,
    topic TEXT,
    completed INTEGER,
    total INTEGER,
    PRIMARY KEY(user_id, topic)
);
