from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database import select, SessionDep
from ..schemas import User
from ..models import Token
from ..utils import authenticate_user
from ..oauth2 import create_access_token


router = APIRouter(
    prefix = "/login",
    tags=['Authentication']
)


@router.post("/", response_model=Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(User, session, user_credentials.username, user_credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"user_id": user.id})
    
    return Token(access_token=access_token, token_type="bearer")
