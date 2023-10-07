import logging
from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from consts import ACCESS_TOKEN_EXPIRE_MINUTES
from database.authentication import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from database.models import Token, User
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

app = FastAPI()


@app.post("/token", response_model=Token)
async def path_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def path_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80)
