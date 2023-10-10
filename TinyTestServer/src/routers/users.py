import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from authentication.user_auth import (
    get_current_user,
)
from database.crud.users import (
    delete_user_api_key,
    get_user_api_key,
    reset_user_api_key,
)
from database.schema.users import User
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def get_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/me/api_key")
async def get_users_me_api_key(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return get_user_api_key(current_user.username)


@router.post("/me/api_key")
async def post_users_me_api_key(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return reset_user_api_key(current_user.username)


@router.delete("/me/api_key")
async def delete_users_me_api_key(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return delete_user_api_key(current_user.username)
