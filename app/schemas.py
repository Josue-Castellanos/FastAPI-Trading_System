from .models import PostBase, UserBase, VoteBase, VoteType
from sqlmodel import Relationship, Field, text
from typing import List, Optional
from datetime import datetime


class User(UserBase, table=True):
    __tablename__ = "users" 

    id: int = Field(default=None, primary_key=True, unique=True, nullable=False)
    created: datetime = Field(nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP")
        }
    )
    last_modified: Optional[datetime] = Field(
        sa_column_kwargs={
            "server_default": text("NULL ON UPDATE CURRENT_TIMESTAMP")
        }
    )
    posts: List["Post"] = Relationship(back_populates="user")
    votes: List["Vote"] = Relationship(back_populates="user")


class Post(PostBase, table=True):
    __tablename__ = "posts" 

    id: int = Field(nullable=False, primary_key=True, unique=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    created: datetime = Field(nullable=False,
        sa_column_kwargs={
            "server_default": text("CURRENT_TIMESTAMP")
        }
    )
    last_modified: Optional[datetime] = Field(
        sa_column_kwargs={
            "server_default": text("NULL ON UPDATE CURRENT_TIMESTAMP")
        }
    )
    user: "User" = Relationship(back_populates="posts")
    votes: List["Vote"] = Relationship(back_populates="post")


class Vote(VoteBase, table=True):
    __tablename__ = "votes" 

    post_id: int = Field(default=None, primary_key=True, foreign_key="posts.id", ondelete="CASCADE")
    user_id: int = Field(default=None, primary_key=True, foreign_key="users.id", ondelete="CASCADE")
    vote_type: VoteType = Field(nullable=False)

    user: "User" = Relationship(back_populates="votes")
    post: Optional[Post] = Relationship(back_populates="votes")





