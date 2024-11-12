from typing import Annotated, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..oauth2 import get_current_user
from ..models import VoteType
from ..schemas import Post, User, Vote
from ..database import select, SessionDep


router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def manage_vote(vote: Vote, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    db_post = session.exec(select(Post).where(Post.id == vote.post_id)).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} not found")
    if vote.vote_type not in VoteType:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid vote type")
    db_vote = session.exec(select(Vote).where(Vote.post_id==vote.post_id, Vote.user_id==current_user.id)).first()
    
    # If Vote exists then user already voted on post
    if db_vote:
        # Change the str to VoteType Enum for delete/update
        vote.vote_type = VoteType(vote.vote_type)
        if db_vote.vote_type == vote.vote_type:
            # Delete the vote
            session.delete(db_vote)
            session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else: 
            # Update the vote type
            vote_data = vote.model_dump(exclude_unset=True)
            db_vote.sqlmodel_update(vote_data)
            session.add(db_vote)
            session.commit()
            session.refresh(db_vote)
            return db_vote
    else:
        # Create vote
        new_vote = Vote(**vote.model_dump())
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
    return new_vote



# Another route to retrieve posts that a user has liked

# Another route to retrieve posts that a user has disliked

