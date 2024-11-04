from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import text


class PostBase(SQLModel):
    user_id: int = Field(nullable=False)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: Optional[bool] = Field(nullable=False, default=True,
        sa_column_kwargs={
            "server_default": text("1")
        }
    )

"""
Schema
"""
class Post(PostBase, table=True):
    id: int = Field(nullable=False, primary_key=True, unique=True)
    created: datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "nullable": False
        }
    )
    last_modified: Optional[datetime] = Field(
        sa_column_kwargs={
            "server_default": text("NULL ON UPDATE CURRENT_TIMESTAMP"),
            "nullable": True
        }
    )


class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class PostPublic(SQLModel):
    title: str
    content: str
    created: datetime
    # last_modified: Optional[datetime]


class PostCreate(PostBase):
    pass

"""
"""

class UserBase(SQLModel):
    # first_name: str = Field(nullable=False)
    # last_name: str = Field(nullable=False)
    # user_name: str = Field(nullable=False, unique=True)
    email: EmailStr = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    # birth_date: datetime = Field(nullable=False)
    # address: str = Field(nullable=False)
    # contact: int = Field(nullable=False)


class User(UserBase, table=True):
    id: int = Field(nullable=False, primary_key=True, unique=True)
    created: datetime = Field(
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP"),
            "nullable": False
        }
    )
    last_modified: Optional[datetime] = Field(
        sa_column_kwargs={
            "server_default": text("NULL ON UPDATE CURRENT_TIMESTAMP"),
            "nullable": True
        }
    )


class UserCreate(UserBase):
    pass


class UserPublic(SQLModel):
    email: EmailStr
    created: datetime
