from typing import Optional

from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.schema.base import DBBase


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    profile_url: Optional[str] = None
    verified: bool = False
    admin: bool = False
    api_key: Optional[str] = None


class RegisteringUser(BaseModel):
    id: str
    name: str
    email: str
    image: str


class DBUser(DBBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(254))
    profile_url: Mapped[str] = mapped_column(String(255))
    verified: Mapped[bool] = False
    admin: Mapped[bool] = False
    api_key: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return (
            f"DBUser("
            f"id={self.id!r}, "
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"profile_url={self.profile_url!r}, "
            f"verified={self.verified!r}, "
            f"admin={self.admin!r}, "
            f"api_key={self.api_key!r}"
            f")"
        )
