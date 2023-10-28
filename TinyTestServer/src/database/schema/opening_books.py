from typing import Optional

from pydantic import BaseModel
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.schema.base import DBBase


class OpeningBookWithoutContents(BaseModel):
    id: int
    name: str


class OpeningBook(OpeningBookWithoutContents):
    contents: str


class DBOpeningBook(DBBase):
    __tablename__ = "opening_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    contents: Mapped[Optional[str]] = mapped_column(Text())

    def __repr__(self) -> str:
        return (
            f"DBOpeningBook("
            f"id={self.id!r}, "
            f"name={self.name!r}), "
            f"contents=<{len(self.contents)} chars>"
            f")"
        )
