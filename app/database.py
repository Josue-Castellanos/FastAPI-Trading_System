from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel, select
from . import models
from .config import DATABASE_URL


def get_session():
    with Session(engine) as db:
        yield db 


engine = create_engine(DATABASE_URL)
SessionDep = Annotated[Session, Depends(get_session)]