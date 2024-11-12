from typing import Annotated
from fastapi import Depends, Response, status, HTTPException, APIRouter
from ..oauth2 import get_current_user
from ..models import UserInDB, UserPublic, UserCreate, UserUpdate
from ..schemas import User
from ..database import select, SessionDep
from ..utils import hash_password


router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)


# USE CASE:// Creates a profile
@router.post("/", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep,):
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  
    return db_user


# Retrieves List of all the existing users in DB
# USE CASE:// Browsing, nothing specific
@router.get("/", response_model=list[UserPublic])
def get_users(session: SessionDep,):
    users = session.exec(select(User)).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No posts exist")
    return users


# Retrieves Active user
# USE CASE:// Displays users information for updating purposes
@router.get("/me", response_model=UserInDB)
def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)],):
    # if current_user.disabled:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="Inactive user")
    return current_user


# Retrieves Singular User using ID, later we will change this to username
# USE CASE:// Searching a specific users profile
@router.get("/{id}", response_model=UserPublic)
def get_user(id: int, session: SessionDep):
    user = session.get(User, id)
    #user = session.exec(select(User).where(User.username == username)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"User with username: {username} not found")
    return user


# Update Active users profile
@router.put("/me", response_model=User, status_code=status.HTTP_201_CREATED)    
def update_user(user: UserUpdate, session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    """
    # This might not be needed since we are retrieving the current user
    # Instead of db_user we use current_user
    db_user = session.get(User, current_user.id)
    if db_user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You do not have permission to update this user")
    """
    user.password = hash_password(user.password)
    user_data = user.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


# Delete active users profile
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)       
def delete_user(session: SessionDep, current_user: Annotated[User, Depends(get_current_user)]):
    session.delete(current_user)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)