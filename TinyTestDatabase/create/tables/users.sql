create table users
(
    id              serial
        constraint users_pk
            primary key,
    username        varchar(255) not null
        constraint users_pk2
            unique,
    hashed_password char(60)     not null
);
