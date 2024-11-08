from typing import Annotated, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..oauth2 import get_current_user
from ..models import PostCreate, PostUpdate, PostPublic, VoteType, Vote
from ..schemas import Post, User
from ..database import select, SessionDep


router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

# USE CASE:// If Vote is 'upvote' remove post from Vote
# Check if a post is already liked by a user
# Check what ENUM type that vote has if its found
# If the vote.vote_type is equal to the vote_type, delete it
# Else if the vote.vote_type is the opostite ENUM Type, update the ENUM type in Vote
# Else insert the newly created vote with its ENUM Type
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: Vote, post_id: int, user_id: int, vote_type: VoteType, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    if vote_type not in VoteType:
        raise HTTPException(status_code=400, detail="Invalid vote type")
    
    db_vote = session.exec((Vote).where(post_id=post_id, user_id=user_id)).first()

    existing_vote = session.exec((Vote).filter_by(post_id=post_id, user_id=user_id)).first()
    if existing_vote:
        raise HTTPException(status_code=400, detail="User has already voted on this post")

    vote = Vote(post_id=post_id, user_id=user_id, vote_type=vote_type)
    
    session.add(vote)
    session.commit()

# Another route to retrieve posts that a user has liked

# Another route to retrieve posts that a user has disliked

# Another route to update the Enum type of a post
# USE CASE:// When a user clicks on a like(ON), then clicks on it again (OFF) -> like a switch
    