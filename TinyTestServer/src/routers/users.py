import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from authentication.user_auth import (
    get_current_user,
)
from database.schema.users import User
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
