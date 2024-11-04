from sqlmodel import create_engine, Session, SQLModel, select
from . import models
import time
import pymysql.cursors
from .config import DATABASE_URL, HOST, USER, PASSWORD, DATABASE


# SQLModel
engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as db:
        yield db 


def connect_to_database():
    while True:
        try:
            connection = pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cursor = connection.cursor()
            print("Connected to Database!")
            return connection, cursor
        except Exception as error:
            print("Connection to Database failed!")
            print("Error: ", error)
            time.sleep(2)
