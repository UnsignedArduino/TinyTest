create table public.sprts
(
    id                        serial
        constraint sprts_pk
            primary key,
    engine_1_git_url          varchar(255)                        not null,
    engine_1_commit           varchar(40)                         not null,
    engine_2_git_url          varchar(255)                        not null,
    engine_2_commit           varchar(40)                         not null,
    elo0                      integer                             not null,
    elo1                      integer                             not null,
    alpha                     numeric                             not null,
    beta                      numeric                             not null,
    max_games                 integer                             not null,
    game_pgns_to_save         integer   default 0                 not null,
    time_control              varchar(16)                         not null,
    opening_book_id           serial
        constraint sprts_opening_books_id_fk
            references public.opening_books,
    games_queued              integer                             not null,
    games_running             integer   default 0                 not null,
    games_finished_white_mate integer   default 0                 not null,
    games_finished_black_mate integer   default 0                 not null,
    games_finished_draw       integer   default 0                 not null,
    games_finished_canceled   integer   default 0                 not null,
    games_finished_error      integer   default 0                 not null,
    result                    text      default 'Queueing'::text  not null,
    scheduled_by              serial
        constraint sprts_users_id_fk
            references public.users,
    queue_time                timestamp default CURRENT_TIMESTAMP not null,
    start_time                timestamp,
    end_time                  timestamp,
    priority                  integer   default 0                 not null,
    paused                    boolean   default false             not null
);

comment on table public.sprts is 'All SPRTs';

comment on column public.sprts.max_games is 'Maximum number of games';

comment on column public.sprts.game_pgns_to_save is 'This is the number of PGNs to save from the games, must be less then or equal to the max amount of games';

comment on column public.sprts.games_queued is 'Number of games left, should start off equaling max_games';

comment on column public.sprts.priority is 'Claimed games come from SPRT with highest priority and then sorted by oldest queue time';

comment on column public.sprts.paused is 'true if paused and no more games should be claimed ';

alter table public.sprts
    owner to postgres;
