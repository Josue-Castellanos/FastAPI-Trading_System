from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from dotenv import load_dotenv
import pymysql.cursors
import os
import time
from pathlib import Path


# CRUD app -> Create, Read, Update, Delete
app = FastAPI()


# Models for Database -> MySQL
class PostModify(BaseModel):
    title: str
    content: str
    published: bool = True


# Instantiate PostModify class
class PostCreate(BaseModel):
    user: int
    body: PostModify


# Load environment variables from .env
load_dotenv(dotenv_path=Path('app/.env'))
HOST = os.getenv("host")
USER = os.getenv("user")
PASSWORD = os.getenv("password")
DATABASE = os.getenv("database")


# Connect to MySQL Database, loop until the connection has established
while True:
    try:
        # Connect to the database
        connection = pymysql.connect(host=HOST,
                                    user=USER,
                                    password=PASSWORD,
                                    database=DATABASE,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        cursor = connection.cursor()
        print("Connected to Database!")
        break
    except Exception as error:
        print("Connection to Database failed!")
        print("Error: ", error)
        time.sleep(2)


# Welcome message = Home Page
@app.get("/")                 # ("/") -> Path Parameter
def root():
    return {"message": "Hello Fellow Engineers, Welcome To My FastAPI"}


# Create == Post
# Creates one singular post
@app.post("/posts", status_code=status.HTTP_201_CREATED)      # ("/posts", status_code=status.HTTP_201_CREATED) -> 
                                                              # Path Parameter and defaults the HTTP status code to 201
def create_post(post: PostCreate):
    query = """
    INSERT INTO posts (user_id, title, content, published) VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (post.user, post.body.title, post.body.content, post.body.published,))
    connection.commit()    

    # Retrieve the newest post
    new_post_id = cursor.lastrowid
    new_post = get_post(new_post_id)
    return {"post_detail": new_post}


# Read == GET
# Retrieve all posts
@app.get("/posts")   
def get_posts():
    query = """
    SELECT * FROM posts
    """
    cursor.execute(query)
    posts = cursor.fetchall()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts not found")
    return {"post_detail": posts}


# Read == GET
# Retrieve one singular Post with ID
@app.get("/posts/{id}")     
def get_post(id: int):          # (id: int) -> Validation to confirm if ID can be automaically turned into an integer, 
                                # if not the built in response will send an error to the front end
    query = """
    SELECT * FROM posts 
    WHERE id = %s
    """
    cursor.execute(query, (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"post_detail" : post}


# Read == GET
# Retrieve the latest singular Post
@app.get("/posts/latest")   
def get_latest_post():
    query = """
    SELECT * FROM posts 
    ORDER BY id DESC LIMIT 1
    """  
    cursor.execute(query)
    latest_post = cursor.fetchone()
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found")
    return {"post_detail" : latest_post}


# Read == GET
# Retrieve the latest singular Post with user ID
@app.get("/posts/latest/user/{user_id}")   
def get_latest_user_post(user_id: int):
    query = """
    SELECT * FROM posts
    WHERE user_id = %s
    ORDER BY id DESC LIMIT 1
    """  
    cursor.execute(query, (user_id,))
    latest_user_post = cursor.fetchone()

    if not latest_user_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {user_id} not found")
    return {"post_detail" : latest_user_post}


# Read == GET
# Retrieve all Post with user ID
@app.get("/posts/user/{user_id}")     
def get_user_posts(user_id: int):          # (user_id: int) -> Validation to confirm if user ID can be automaically turned into an integer, 
                                           # if not the built in response will send an error to the front end
    query = """
    SELECT * FROM posts 
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    posts = cursor.fetchall()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with user_id: {user_id} not found")
    return {"post_detail" : posts}


# Update == PUT
# Update one singular Post with ID
@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)     # ("/posts/{id}", status_code=status.HTTP_201_CREATED) -> 
                                                                 # Path Parameter and defaults the HTTP status code to 201
def update_post(id: int, post: PostModify):
    # CHECK:// If post exists
    get_post(id)
    
    query = """
    UPDATE posts 
    SET title = %s, content = %s, published = %s 
    WHERE id = %s
    """
    cursor.execute(query, (post.title, post.content, post.published, id,))
    connection.commit()
    updated_post = get_post(id)
    return {"data": updated_post}


# Delete == DELETE
# Delete one singular Post with ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)       # ("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) -> 
                                                                         # Path Parameter and default the HTTP status code to 204
def delete_post(id: int):          # (id: int) -> Validation to confirm if ID can be automaically turned into an integer, 
                                   # if not the built in response will send an error to the front end
    # CHECK:// If post exists
    get_post(id)
    
    query = """
    DELETE FROM posts 
    WHERE id = %s
    """
    cursor.execute(query, (id,))
    connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
