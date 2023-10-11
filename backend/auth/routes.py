"""
Module containing routes and handlers for auth
"""


from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt

from config import settings
from models.user import User, User_Pydantic, UserCreate

from .services import authenticate_user, get_current_user
from .token import (
    TokenResponse,
    refresh_tokens,
    create_tokens,
)

auth_router = APIRouter()
JWT_SECRET = settings.SECRET_KEY


@auth_router.post("/token", tags=["auth"], response_model=TokenResponse)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user
    :param form_data: username and login
    :return: access and refresh tokens and token type
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return await create_tokens(user)


@auth_router.post("/refresh_token", tags=["auth"], response_model=TokenResponse)
async def get_new_tokens(token: str = Header(...)):
    """
    Refresh tokens
    :param token: refresh token
    :return: new access and refresh tokens
    """
    return await refresh_tokens(token)


@auth_router.post("/register", response_model=User_Pydantic, tags=["auth"])
async def create_user(user: UserCreate):
    """
    Create new user

    :param user: user info for create
    :return: new user if created or error
    """
    user_obj = User(
        username=user.username, password=bcrypt.hash(user.password), email=user.email
    )
    await user_obj.save()
    return user_obj


@auth_router.get("/users/me", response_model=User_Pydantic, tags=["auth"])
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    """
    get user
    :param user: user
    :return: user
    """
    return user
