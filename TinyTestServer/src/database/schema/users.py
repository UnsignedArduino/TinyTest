from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    hashed_password: str


class User(UserCreate):
    id: int

    class Config:
        from_attributes = True
