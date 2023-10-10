import logging
from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from authentication.models import Token
from consts import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from database.crud.users import (
    get_user_by_username,
    get_user_jwt_session,
    set_user_jwt_session,
)
from database.schema.users import User
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/sign-in")


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user_and_get_token(username: str, password: str) -> Token:
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username}, expires_delta=access_token_expires
    )
    set_user_jwt_session(username, access_token)
    return Token(access_token=access_token, token_type="bearer")


def authenticate_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        db_jwt = get_user_jwt_session(username)
        if db_jwt != token:
            logger.debug(f"JWT session for {username} does not match database!")
            return None
        logger.debug(f"JWT session validated!")
        return username
    except JWTError:
        logger.debug(f"Invalid JWT session, expired?")
        return None


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    username = authenticate_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find username!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_verified_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.verified:
        raise HTTPException(status_code=403, detail="Unverified user")
    return current_user


async def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.admin:
        raise HTTPException(status_code=403, detail="Non-admin user")
    return current_user
