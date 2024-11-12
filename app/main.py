from fastapi import FastAPI
from .database import engine, SQLModel
from .routers  import post, user, auth, vote

# SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

app = FastAPI()

#connect_to_database()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Home page"}

   
