from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column, BigInteger
from typing import Optional
from datetime import datetime
from sqlalchemy import text
from enum import Enum as PyEnum


"""
Post Models
"""
class PostBase(SQLModel):
    id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: Optional[bool] = Field(nullable=False, default=True,
        sa_column_kwargs={
            "server_default": text("1")})


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class PostPublic(SQLModel):
    # username: str
    title: str
    content: str
    created: datetime
    last_modified: Optional[datetime]
    upvotes: int
    downvotes: int
    # owner: PostBase    


class PostCreate(PostBase):
    pass


"""
User Models
"""
class UserBase(SQLModel):
    id: Optional[int] = Field(default=None)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    user_name: Optional[str] = Field(default=None, unique=True)
    birth_date: Optional[datetime] = Field(default=None)
    address: Optional[str] = Field(default=None)
    contact: Optional[int] = Field(default=None, sa_column=Column(BigInteger))
    # disabled: Optional[bool] = Field(default=None, nullable=True)


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    address: Optional[str] = None
    contact: Optional[int] = None
    # disabled: Optional[bool] = None


class UserCreate(UserBase):
    pass


class UserPublic(SQLModel):
    email: EmailStr
    created: datetime


class UserInDB(UserBase):
    hashed_password: str

"""
Token
"""
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: int

"""
Votes
"""
class VoteBase(SQLModel):
    post_id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)

class VoteType(PyEnum):
    upvote = "upvote"
    downvote = "downvote"



