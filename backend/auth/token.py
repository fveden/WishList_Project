import time

import jwt
from config import settings
from fastapi import HTTPException, status
from models.user import RefreshToken, User, User_Pydantic
from pydantic import BaseModel

JWT_SECRET = settings.SECRET_KEY
ALGORITHM = 'HS256'


async def create_access_token(user: User):
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    sub = user_obj.dict()
    sub['scope'] = 'access'
    token_expiry_minutes = 30
    sub['exp'] = time.time() + 60 * token_expiry_minutes
    access_token = jwt.encode(sub, JWT_SECRET, algorithm=ALGORITHM)
    return access_token


async def create_refresh_token(user: User):
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    sub = user_obj.dict()
    sub['scope'] = 'refresh'
    token_expiry_days = 30
    sub['exp'] = time.time() + 86400 * token_expiry_days
    print(time.time())
    refresh_token = jwt.encode(sub, JWT_SECRET, algorithm=ALGORITHM)
    refresh_token_db = await RefreshToken.get_or_none(user=user)
    if refresh_token_db is None:
        await RefreshToken.create(user=user, refresh_token=refresh_token)
    else:
        refresh_token_db.token = refresh_token
        await refresh_token_db.save()
    return refresh_token


async def refresh_tokens(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=ALGORITHM)
        if payload.get('scope') != "refresh":
            raise jwt.exceptions.InvalidTokenError
        print(payload.get('id'))
        user = await User.get(username=payload.get('username'))
        access_token = await create_access_token(user)
        refresh_token = await create_refresh_token(user)
        return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username of password")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
