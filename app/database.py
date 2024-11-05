from sqlmodel import create_engine, Session, SQLModel, select
from . import models
import time
from sqlalchemy.exc import OperationalError
from .config import DATABASE_URL


engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as db:
        yield db 


def connect_to_database():
    while True:
        try:
            # Try connecting to the database
            with engine.connect() as connection:
                print("Connected to Database!")
                break  # Exit loop if successful
        except OperationalError as error:
            print("Connection to Database failed! Retrying in 2 seconds...")
            print("Error:", error)
            time.sleep(2)