CREATE TABLE users
(
    id          SERIAL
        CONSTRAINT users_pk
            PRIMARY KEY,
    username    VARCHAR(255)          NOT NULL
        CONSTRAINT users_pk2
            UNIQUE,
    profile_url VARCHAR(255),
    verified    BOOLEAN DEFAULT FALSE NOT NULL,
    admin       BOOLEAN DEFAULT FALSE NOT NULL,
    api_key     CHAR(64)
        CONSTRAINT users_pk3
            UNIQUE
);


