
CREATE TABLE IF NOT EXISTS quiz_progress(
    user_id INTEGER,
    topic TEXT,
    current_question INTEGER,
    PRIMARY KEY(user_id, topic)
);
