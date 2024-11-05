from typing import Annotated
from fastapi import Response, status, HTTPException, Depends, APIRouter
from ..models import UserPublic, User, UserCreate
from ..database import get_session, Session, select


router = APIRouter(
    prefix = "/users"
)
SessionDep = Annotated[Session, Depends(get_session)]

"""
Users
"""
@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep,):
    hashed_password = hash(user.password)
    user.password = hashed_password

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  
    return db_user


@router.get("/", response_model=list[UserPublic])
def get_users(session: SessionDep,):
    users = session.exec(select(User)).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No posts exist")
    return users


@router.get("/{id}", response_model=UserPublic)
def get_user(id: int, session: SessionDep):
    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    
    # verify user here?

    return user