from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class User(UserCreate):
    id: int
    verified: bool = False
    admin: bool = False

    class Config:
        from_attributes = True
