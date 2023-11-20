
from typing import List
from fastapi import APIRouter, status
from schemas import AuthorCreate, AuthorOut, AuthorUpdate
from crud.authors import author

router = APIRouter()

@router.get("/", response_model=List[AuthorOut], status_code=status.HTTP_200_OK)
async def get_multiple_authors(
    skip: int = 0,
    limit: int = 10,
):
    authors = await author.get_many(skip, limit)
    return [{**AuthorOut(**author).dict()} for author in authors]

@router.post("/", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
async def create_new_author(author_in: AuthorCreate):
    new_generated_id = await author.create(author_in)
    return {**author_in.dict(), "id": new_generated_id}