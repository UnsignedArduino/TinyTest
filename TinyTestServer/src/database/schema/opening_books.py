from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Enum as SAEnum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.schema.base import DBBase


class CompressionFormatEnum(str, Enum):
    none = "none"
    zip = "zip"


class BookFormatEnum(str, Enum):
    pgn = "pgn"
    epd = "epd"


class OpeningBookWithoutContents(BaseModel):
    id: int
    name: str
    compression_format: CompressionFormatEnum
    book_format: BookFormatEnum


class OpeningBook(OpeningBookWithoutContents):
    contents: str


class DBOpeningBook(DBBase):
    __tablename__ = "opening_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    contents: Mapped[Optional[str]] = mapped_column(Text())
    compression_format: Mapped[SAEnum[CompressionFormatEnum]] = mapped_column(
        SAEnum(CompressionFormatEnum)
    )
    book_format: Mapped[SAEnum[BookFormatEnum]] = mapped_column(SAEnum(BookFormatEnum))

    def __repr__(self) -> str:
        return (
            f"DBOpeningBook("
            f"id={self.id!r}, name={self.name!r}), "
            f"compression_format={self.compression_format!r}, "
            f"book_format={self.book_format!r}"
            f")"
        )
