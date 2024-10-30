from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select



# PyMySQL
PYMYSQL_DATABSE_URL = 'mysql+pymysql://scott:tiger@localhost/foo'
engine = create_engine(PYMYSQL_DATABSE_URL)

# default
MYSQL_DATABASE_URL = 'mysql://scott:tiger@localhost/foo'
engine = create_engine(MYSQL_DATABASE_URL)


DATABASE_URL = "mysql+mysqlconnector://root:password@localhost/mydatabase"
engine = create_engine(DATABASE_URL)
