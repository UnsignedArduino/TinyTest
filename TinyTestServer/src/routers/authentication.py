import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from authentication.models import Token
from authentication.user_auth import (
    authenticate_user_and_get_token,
    get_password_hash,
)
from database.crud.users import create_user, get_user_by_username
from database.schema.users import UserCreate
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


router = APIRouter(prefix="/authentication", tags=["authentication"])


@router.post("/sign-in", response_model=Token)
async def post_sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return authenticate_user_and_get_token(form_data.username, form_data.password)


@router.post("/sign-up", response_model=Token)
async def post_sign_up(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if get_user_by_username(form_data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    create_user(
        UserCreate(
            username=form_data.username,
            hashed_password=get_password_hash(form_data.password),
        )
    )
    return authenticate_user_and_get_token(form_data.username, form_data.password)
