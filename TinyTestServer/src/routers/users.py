import logging
import secrets
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Header, status

from consts import API_KEY_LENGTH
from database.crud.users import (
    id_set_api_token,
    id_to_api_token,
    is_api_key_system,
    is_user_id_admin,
    is_user_id_registered,
    is_user_id_system,
    is_user_id_verified,
    register_user,
)
from database.schema.users import RegisteringUser
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


StringHeader = Annotated[str | None, Header()]


@router.post(
    "/register_user",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Register a user to keep record of all users ever signed in.",
)
async def post_register_user(
    registering_user: RegisteringUser,
    x_api_token: StringHeader = None,
):
    if (
        not is_api_key_system(x_api_token)
        or registering_user.id == "1"
        or registering_user.name == "system"
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    register_user(registering_user)


@router.post(
    "/id_to_api_token",
    summary="Get the API token from a user id.",
)
async def post_id_to_api_token(
    user_id: Annotated[int, Body()],
    x_api_token: StringHeader = None,
):
    if not is_api_key_system(x_api_token) or user_id == 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = id_to_api_token(user_id)
    if token is None:
        token = secrets.token_hex(API_KEY_LENGTH)
        id_set_api_token(user_id, token)
    return {"api_token": token}


@router.post(
    "/id_regenerate_api_token",
    summary="Regenerate the API token for a user.",
)
async def post_id_regenerate_api_token(
    user_id: Annotated[int, Body()],
    x_api_token: StringHeader = None,
):
    if not is_api_key_system(x_api_token) or user_id == 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = secrets.token_hex(API_KEY_LENGTH)
    id_set_api_token(user_id, token)
    return {"api_token": token}


@router.get(
    "/roles",
    summary="Get roles for a user.",
)
async def get_roles(user_id: int):
    return {
        "registered": is_user_id_registered(user_id),
        "verified": is_user_id_verified(user_id),
        "admin": is_user_id_admin(user_id),
        "system": is_user_id_system(user_id),
    }
