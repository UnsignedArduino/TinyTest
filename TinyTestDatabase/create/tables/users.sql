create table public.users
(
    id              serial
        constraint users_pk
            primary key,
    username        varchar(255) not null,
    hashed_password char(60)     not null
);

alter table public.users
    owner to postgres;
