INSERT INTO users(username) VALUES("Test User");

INSERT INTO
    user_auth (user_id, email, hashed_password)
SELECT
    user_id,
    "test@email.com",
    ""
FROM users WHERE username = "Test User";

INSERT
    sessions(user_id, started, ended)
SELECT
    user_id,
    NOW(),
    NULL
FROM users WHERE username = "Test User";
