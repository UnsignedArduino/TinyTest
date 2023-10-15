from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    profile_url: Optional[str] = None
    verified: bool = False
    admin: bool = False
    api_key: Optional[str] = None


class RegisteringUser(BaseModel):
    id: str
    name: str
    email: str
    image: str
