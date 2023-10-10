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
    api_key         CHAR(64)
        CONSTRAINT users_pk3
            UNIQUE
);


