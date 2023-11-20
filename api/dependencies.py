from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import jwt

from schemas import TokenPayload
from models import Client
from settings import settings
from crud.clients import client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_v1_STR}/clients/sign_in")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Client:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate credentials",
        )
    return await client.get_one_by_email(email=token_data.sub)
