import logging

from sqlalchemy import text

from database.connection import engine
from database.schema.users import RegisteringUser
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def is_user_id_registered(user_id: int) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text("SELECT COUNT(id) FROM users WHERE id=:id"), {"id": user_id}
            ).all()[0][0]
            > 0
        )


def is_user_id_verified(user_id: int) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text("SELECT COUNT(id) FROM users WHERE id=:id AND verified=TRUE"),
                {"id": user_id},
            ).all()[0][0]
            > 0
        )


def is_user_id_admin(user_id: int) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text(
                    "SELECT COUNT(id) FROM users "
                    "WHERE id=:id AND verified=TRUE AND admin=TRUE"
                ),
                {"id": user_id},
            ).all()[0][0]
            > 0
        )


def is_user_id_system(user_id: int) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text(
                    "SELECT COUNT(id) FROM users "
                    "WHERE id=:id AND username='system' "
                    "AND verified=TRUE AND admin=TRUE"
                ),
                {"id": user_id},
            ).all()[0][0]
            > 0
        )


def is_api_key_verified(api_key: str) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text(
                    "SELECT COUNT(id) FROM users "
                    "WHERE api_key=:api_key AND verified=TRUE"
                ),
                {"api_key": api_key},
            ).all()[0][0]
            > 0
        )


def is_api_key_admin(api_key: str) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text(
                    "SELECT COUNT(id) FROM users "
                    "WHERE api_key=:api_key AND verified=TRUE AND admin=TRUE"
                ),
                {"api_key": api_key},
            ).all()[0][0]
            > 0
        )


def is_api_key_system(api_key: str) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text(
                    "SELECT COUNT(id) FROM users "
                    "WHERE api_key=:api_key AND username='system' "
                    "AND verified=TRUE AND admin=TRUE"
                ),
                {"api_key": api_key},
            ).all()[0][0]
            > 0
        )


def register_user(user: RegisteringUser):
    logger.debug(f"Registering user {user}")
    with engine.begin() as conn:
        already_registered = is_user_id_registered(int(user.id))
        logger.debug(
            "User already registered, updating values"
            if already_registered
            else "User not registered, inserting values"
        )
        conn.execute(
            text(
                "UPDATE users "
                "SET username=:username, email=:email, profile_url=:profile_url "
                "WHERE id=:id"
            )
            if already_registered
            else text(
                "INSERT INTO users (id, username, email, profile_url) "
                "VALUES (:id, :username, :email, :profile_url)"
            ),
            {
                "id": int(user.id),
                "username": user.name,
                "email": user.email,
                "profile_url": user.image,
            },
        )
