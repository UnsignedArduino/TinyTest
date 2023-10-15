import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Header, status

from database.crud.users import is_api_key_system, register_user
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
