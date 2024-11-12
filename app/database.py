from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session, SQLModel, select
from . import models
from .config import settings


def get_session():
    with Session(engine) as db:
        yield db 

engine = create_engine(settings.DATABASE_URL)
SessionDep = Annotated[Session, Depends(get_session)]