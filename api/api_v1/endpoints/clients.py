from typing import List, Optional
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from schemas import ClientOut, ClientCreate, ClientInDB, Token, ClientUpdate
from models import Client
from api.dependencies import get_current_user
from crud.clients import client
from settings import settings
from utils.auth import create_access_token, verify_password, get_password_hash

router = APIRouter()


@router.get("/me", response_model=ClientOut, status_code=status.HTTP_200_OK)
async def get_user_me(current_user: Client = Depends(get_current_user)):
    return current_user

@router.put("/{client_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user_me(
    client_id: int,
    user_update: ClientUpdate,
    current_user: Client = Depends(get_current_user),
):
    if not await client.get_one(client_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await client.update(client_id, user_update)
    return {**user_update.dict(exclude_unset=True), "id": client_id}

@router.post("/sign_up", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_in: ClientCreate):
    user_info = await client.get_one_by_email(user_in.email)
    if user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already taken",
        )
    user_info = await client.get_one_by_username(user_in.username)
    if user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken",
        )
    user_dict = user_in.dict(exclude={"password"})
    password = get_password_hash(user_in.password)
    user_dict.update({"password": password, "is_superuser": False})
    new_generated_id = await client.create(ClientInDB(**user_dict))
    return {**user_in.dict(), "id": new_generated_id}


@router.post("/sign_in", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data)
    user_info = await client.get_one_by_email(email=form_data.username)
    print(user_info)
    if not user_info or not verify_password(form_data.password, user_info.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user_info.email, access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}