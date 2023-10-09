CREATE TABLE users
(
    id              SERIAL
        CONSTRAINT users_pk
            PRIMARY KEY,
    username        VARCHAR(255)          NOT NULL
        CONSTRAINT users_pk2
            UNIQUE,
    hashed_password CHAR(60)              NOT NULL,
    verified        BOOLEAN DEFAULT FALSE NOT NULL,
    admin           BOOLEAN DEFAULT FALSE NOT NULL,
    session_jwt     VARCHAR(255)
);

COMMENT ON COLUMN users.session_jwt IS 'JWT session to check against incoming requests, can be null if not signed in.';


