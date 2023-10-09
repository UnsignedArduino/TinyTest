import logging
from typing import Optional

from sqlalchemy import text

from database.connection import engine
from database.schema.users import User, UserCreate
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def get_user_by_id(user_id: int) -> Optional[User]:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE id=:id"),
            {"id": user_id},
        ).first()
        if result:
            return User.model_validate(result)


def get_user_by_username(username: str) -> Optional[User]:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM users WHERE username=:username"),
            {"username": username},
        ).first()
        if result:
            return User.model_validate(result)


def create_user(user: UserCreate):
    logger.debug(f"Creating user {user.username} with hashed password")
    with engine.begin() as conn:
        conn.execute(
            text(
                "INSERT INTO users (username, hashed_password) "
                "VALUES (:username, :hashed_password)"
            ),
            {"username": user.username, "hashed_password": user.hashed_password},
        )


def delete_user(user_id: int):
    logger.debug(f"Deleting user with ID {user_id}")
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM users WHERE id=:id"), {"id": user_id})
