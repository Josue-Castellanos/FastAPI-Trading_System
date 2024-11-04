from random import randrange
from typing import Annotated
from fastapi import FastAPI, Query, Response, status, HTTPException, Depends
from pydantic import BaseModel
from .models import Post, PostCreate, PostUpdate, PostPublic, UserPublic, User, UserCreate
from .database import engine, get_session, SQLModel, Session, connect_to_database, select


SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

connection, cursor = connect_to_database()

"""
Posts
"""
@app.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: SessionDep,):
    db_post = Post(**post.model_dump())
    session.add(db_post)
    session.commit()
    session.refresh(db_post)  
    return db_post


@app.get("/posts", response_model=list[PostPublic])   
def get_posts(session: SessionDep,):
    posts = session.exec(select(Post)).all()
    
    if not posts:
        raise HTTPException(status_code=404, detail="No posts exist")
    return posts


@app.get("/posts/latest", response_model=PostPublic)   
def get_latest_post(session: SessionDep,):
    latest_post = session.exec(select(Post).order_by(Post.id.desc()).limit(1)).first()

    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found")
    return latest_post


@app.get("/posts/{id}", response_model=PostPublic)     
def get_post(id: int, session: SessionDep,):          
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return post


@app.get("/posts/latest/user/{user_id}", response_model=PostPublic)   
def get_latest_user_post(user_id: int, session: SessionDep):
    latest_user_post = session.exec(select(Post).where(Post.user_id == user_id).order_by(Post.id.desc()).limit(1)).first()

    if not latest_user_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {user_id} not found")
    return latest_user_post


@app.get("/posts/user/{user_id}", response_model=list[PostPublic])     
def get_user_posts(user_id: int, session: SessionDep,):        
    posts = session.exec(select(Post).where(Post.user_id == user_id)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with user_id: {user_id} not found")
    return posts


@app.put("/posts/{id}", response_model=PostPublic, status_code=status.HTTP_201_CREATED)    
def update_post(id: int, post: PostUpdate, session: SessionDep):
    db_post = get_post(id, session)
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)       
def delete_post(id: int, session: SessionDep):         
    post = get_post(id, session)
    
    session.delete(post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""
Users
"""
@app.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep,):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  
    return db_user