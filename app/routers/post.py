from typing import Annotated, Optional
from sqlmodel import func
from fastapi import Response, status, HTTPException, Depends, APIRouter, Query
from ..oauth2 import get_current_user
from ..models import PostCreate, PostUpdate, PostPublic
from ..schemas import Post, User, Vote
from ..database import select, SessionDep


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

"""
    **THESE ENDPOINTS ARE COMPLETE**
    **WORK IN PROGRESS:// INCLUDE THE USERNAME OF OWNER FOR EACH POST**
"""
# User Creates a Post
@router.post("/", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    post.user_id = current_user.id
    new_post = Post(**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    db_post = get_post(new_post.id, session, current_user)
    return db_post


# Get all posts in Database using pagination
# Default: limit <= 100 & max = 100, offsett(skip) = 0, searching str = ""
@router.get("/all", response_model=list[PostPublic])   
def get_posts(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)], 
              limit: Annotated[int, Query(le=100)] = 100, offset: int = 0, search: Optional[str] = ""):
    posts = session.exec(
        select(Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Post.title.contains(search))
               .group_by(Post.id)
               .offset(offset)
               .limit(limit)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Post not found")
    return posts


# Get the latest singular post in Database
@router.get("/latest", response_model=PostPublic)   
def get_latest_post(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):    
    latest_post = session.exec(
        select(Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Post.user_id == current_user.id)
               .group_by(Post.id)
               .order_by(Post.id.desc())
               .limit(1)).first()

    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found")
    return latest_post


# Get all posts active user has upvoted
@router.get("/upvote", response_model=list[PostPublic])
def get_upvote_posts(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    upvoted_posts = session.exec(
        select(Vote.user_id, Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Vote.user_id == current_user.id)
               .group_by(Post.id)
               .having(func.sum(Vote.vote_type == 'upvote') > 0)).all()
    if not upvoted_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with upvotes not found")
    return upvoted_posts
    

# Get all posts active user has downvoted
@router.get("/downvote", response_model=list[PostPublic])
def get_downvote_posts(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    downvoted_posts = session.exec(
        select(Vote.user_id, Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Vote.user_id == current_user.id)
               .group_by(Post.id)
               .having(func.sum(Vote.vote_type == 'downvote') > 0)).all()
    if not downvoted_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts with downvotes not found")
    return downvoted_posts


# Get all active user posts
@router.get("/me", response_model=list[PostPublic])     
def get_current_user_posts(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):        
    posts = session.exec(
        select(Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Post.user_id == current_user.id)
               .group_by(Post.id)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Posts from Current User not found")
    return posts
    

# Get the latest singular user post using User_ID
@router.get("/latest/user/{user_id}", response_model=PostPublic)   
def get_latest_user_post(user_id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found or does not exist")
    latest_user_post = session.exec(
        select(Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Post.user_id == user_id)
               .group_by(Post.id)
               .order_by(Post.id.desc())
               .limit(1)).first()
    if not latest_user_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post from User {user_id} not found")
    return latest_user_post


# Get all user posts using User ID
@router.get("/user/{user_id}", response_model=list[PostPublic])
def get_user_posts(user_id: int, session: SessionDep, ):
    """
    SELECT p.user_id, p.id, p.title, p.content, p.created, p.last_modified,
    COALESCE(SUM(v.vote_type = 'upvote'), 0) AS upvotes,
    COALESCE(SUM(v.vote_type = 'downvote'), 0) AS downvotes
    FROM 
        posts p
    LEFT JOIN 
        votes v ON p.id = v.post_id
    WHERE 
        p.user_id = 2
    GROUP BY 
        p.id;
    """
    posts = session.exec(
        select(Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Post.user_id == user_id).group_by(Post.id)).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts from User {user_id} not found")
    return posts


# Get a single post using Post ID
@router.get("/{id}", response_model=PostPublic)     
def get_post(id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):          
    post = session.exec(
        select(Post.user_id, Post.id, Post.title, Post.content, Post.created, Post.last_modified,
               func.coalesce(func.sum(Vote.vote_type == 'upvote'), 0).label('upvotes'),
               func.coalesce(func.sum(Vote.vote_type == 'downvote'), 0).label('downvotes'))
               .join(Vote, Vote.post_id == Post.id, isouter=True)
               .filter(Post.id == id)
               .group_by(Post.id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found")
    return post


# Update a singular post
@router.put("/{id}", response_model=PostPublic, status_code=status.HTTP_201_CREATED)    
def update_post(id: int, post: PostUpdate, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    db_post = get_post(id, session, current_user)

    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# Delete a singular post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)       
def delete_post(id: int, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):         
    db_post = get_post(id, session, current_user)
    
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    session.delete(db_post)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


