import logging
from typing import Optional

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from database.connection import engine
from database.schema.opening_books import (
    DBOpeningBook,
    OpeningBookWithoutContents,
)
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def book_id_exist(book_id: int) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text("SELECT COUNT(id) FROM opening_books WHERE id=:id"),
                {"id": book_id},
            ).first()[0]
            > 0
        )


def id_get_book(book_id: int) -> Optional[OpeningBookWithoutContents]:
    with Session(engine) as session:
        result = session.execute(
            select(
                DBOpeningBook.id,
                DBOpeningBook.name,
            ).where(DBOpeningBook.id == book_id)
        ).first()
        if result is None:
            return None
        else:
            return OpeningBookWithoutContents(**result._mapping)


def id_get_all_books() -> list[OpeningBookWithoutContents]:
    with Session(engine) as session:
        result = session.execute(select(DBOpeningBook.id, DBOpeningBook.name))
        books = []
        for row in result:
            books.append(OpeningBookWithoutContents(**row._mapping))
        return books


def id_get_book_contents(book_id: int) -> Optional[str]:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT (contents) FROM opening_books WHERE id=:id"),
            {"id": book_id},
        ).first()
        if result is None:
            return None
        else:
            return result[0]


def id_set_book(book: OpeningBookWithoutContents) -> int:
    with engine.begin() as conn:
        book_exists = book_id_exist(book.id)
        logger.debug(
            f"Updating book {book.id} with name {book.name}"
            if book_exists
            else f"Registering new book with name {book.name}"
        )
        if book_exists:
            conn.execute(
                text("UPDATE opening_books SET name=:name WHERE id=:id"),
                {
                    "name": book.name,
                    "id": book.id,
                },
            )
            return book.id
        else:
            result = conn.execute(
                text("INSERT INTO opening_books (name) VALUES (:name) RETURNING id"),
                {"name": book.name},
            ).first()
            return int(result[0])


def id_set_book_contents(book_id: int, book: Optional[str] = None):
    with engine.begin() as conn:
        logger.debug(f"Updating book contents for book id {book_id}")
        conn.execute(
            text("UPDATE opening_books SET contents=:contents WHERE id=:id"),
            {
                "contents": book,
                "id": book_id,
            },
        )


def id_delete_book(book_id: int):
    with engine.begin() as conn:
        logger.debug(f"Deleting book for book id {book_id}")
        conn.execute(
            text("DELETE FROM opening_books WHERE id=:id"),
            {
                "id": book_id,
            },
        )
