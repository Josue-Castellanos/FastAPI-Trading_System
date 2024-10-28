from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel


# CRUD app -> Create, Read, Update, Delete
# Top Down Structre, meaning FastAPI is going down the list of all our request paths and choose the first one that matches first, order matters
app = FastAPI()


# SCHEMA for Database -> MySQL
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# In reality we will save this data in the databse but we will keep it simple and save it in memory, Globally using an array that holds objects
my_post = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1}, 
           {"title" : "favorite foods", "content" : "I like pizza", "id" : 2}]


# Helper functions
def find_post(id):
    return next((post for post in my_post if post["id"] == id), None)


def find_index_post(id):
    return next((index for index, post in enumerate(my_post) if post["id"] == id), None)


# Read == GET
@app.get("/")                 # ("/") -> Path Parameter
def root():
    return {"message": "Hello Fellow Engineers, Welcome To My FastAPI"}


# Read == GET
# Retrieves all posts
@app.get("/posts")            # ("/posts") -> Path Parameter
def get_posts():
    return {"data": my_post}


# Create == Post
# Creates one singular post
@app.post("/posts", status_code=status.HTTP_201_CREATED)      # ("/posts", status_code=status.HTTP_201_CREATED) -> Path Parameter and defaults the HTTP status code to 201
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)    # randrange(0, 1000000) -> MySQL will make a Unique ID in the databse but for now we will make a random ID, manually
    my_post.append(post_dict)      
    return {"data": post_dict}


# Read == GET
# Retrieves the latest singular Post
@app.get("/posts/latest")     # ("/posts/latest") -> Path Parameter
def get_latest_posts():          
    post = my_post[len(my_post) - 1]
    return {"post_detail" : post}


# Read == GET
# Retrieves one singular Post with ID
@app.get("/posts/{id}")       # ("/posts/{id}") -> Path Parameter
def get_posts(id: int):          # (id: int) -> Validation to confirm if ID can be automaically turned into an integer, if not the built in response will send an error to the front end
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"post_detail" : post}


# Delete == DELETE
# Deletes one singular Post with ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)       # ("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) -> Path Parameter and default the HTTP status code to 204
def delete_posts(id: int):          # (id: int) -> Validation to confirm if ID can be automaically turned into an integer, if not the built in response will send an error to the front end
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update == PUT
# Updates one singular Post with ID
@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)     # ("/posts/{id}", status_code=status.HTTP_201_CREATED) -> Path Parameter and defaults the HTTP status code to 201
def update_posts(id: int, post: Post):
    index = find_index_post(id)
    if not index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {"data": post_dict}