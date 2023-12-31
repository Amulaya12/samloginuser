from typing import List
from pydantic import BaseModel


class UserInfoBase(BaseModel):
    username: str
    fullname: str


class UserCreate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        from_attributes = True

class UserAuthenticate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str