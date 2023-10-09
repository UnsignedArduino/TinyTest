CREATE TABLE users
(
    id              SERIAL
        CONSTRAINT users_pk
            PRIMARY KEY ,
    username        VARCHAR(255) NOT NULL
        CONSTRAINT users_pk2
            UNIQUE ,
    hashed_password CHAR(60)     NOT NULL
);
