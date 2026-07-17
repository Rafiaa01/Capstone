CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done)
VALUES
    ('Learn FastAPI', FALSE),
    ('Build a Task API', FALSE),
    ('Push the project to GitHub', TRUE);