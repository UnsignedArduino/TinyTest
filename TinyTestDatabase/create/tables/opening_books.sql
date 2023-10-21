CREATE TYPE COMPRESSIONFORMAT AS ENUM ('none', 'zip');
CREATE TYPE BOOKFORMAT AS ENUM ('pgn', 'epd');

CREATE TABLE opening_books
(
    id                 SERIAL
        CONSTRAINT opening_books_pk
            PRIMARY KEY,
    name               VARCHAR(255)                                        NOT NULL
        CONSTRAINT opening_books_pk2
            UNIQUE,
    contents           TEXT,
    compression_format COMPRESSIONFORMAT DEFAULT 'none'::COMPRESSIONFORMAT NOT NULL,
    book_format        BOOKFORMAT        DEFAULT 'pgn'::BOOKFORMAT         NOT NULL
);

COMMENT ON COLUMN opening_books.contents IS 'Base85 contents of book, could be PGN, EPD, compressed, etc.';
