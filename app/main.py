from typing import Annotated
from fastapi import FastAPI, Depends
from .database import engine, get_session, SQLModel, Session, connect_to_database
from .routers  import post, user



SQLModel.metadata.create_all(engine)

# SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

connect_to_database()
app.include_router(post.router)
app.include_router(user.router)


   
