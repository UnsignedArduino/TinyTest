from typing import Union

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class User(UserCreate):
    id: int
    verified: bool = False
    admin: bool = False
    session_jwt: Union[str, None]
    api_key: Union[str, None]

    class Config:
        from_attributes = True
