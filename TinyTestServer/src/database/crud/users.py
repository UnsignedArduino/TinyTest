import logging
import secrets
from typing import Optional

from sqlalchemy import text

from consts import API_KEY_LENGTH
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


def reset_user_api_key(username: str):
    with engine.begin() as conn:
        logger.debug(f"Setting new API key for {username}")
        conn.execute(
            text("UPDATE users SET api_key = :api_key WHERE username = :username"),
            {"api_key": secrets.token_hex(API_KEY_LENGTH), "username": username},
        )


def delete_user_api_key(username: str):
    with engine.begin() as conn:
        logger.debug(f"Deleting API key for {username}")
        conn.execute(
            text("UPDATE users SET api_key = null WHERE username = :username"),
            {"username": username},
        )


def get_user_api_key(username: str) -> Optional[str]:
    with engine.connect() as conn:
        logger.debug(f"Getting API key for {username}")
        result = conn.execute(
            text("SELECT api_key FROM users WHERE username=:username"),
            {"username": username},
        ).first()[0]
        if result and len(result) > 0:
            return result


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
