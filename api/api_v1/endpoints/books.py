from typing import List, Optional
from fastapi import APIRouter, Response, HTTPException, status
from schemas import BookCreate, BookOut, BookUpdate
from crud.books import book
from crud.authors import author

router = APIRouter()

@router.get("/", response_model=List[BookOut], status_code=status.HTTP_200_OK)
async def get_multiple_books(
    skip: int = 0,
    limit: int = 10,
):
    books = await book.get_many(skip, limit)
    return [BookOut(**book).dict() for book in books]

@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def create_new_book(book_in: BookCreate):
    new_generated_id = await book.create(book_in)
    created_book = await book.get_one_by_id(new_generated_id)
    return created_book

@router.post("/{author_id}/books", response_model=List[BookOut], status_code=status.HTTP_201_CREATED)
async def create_books_for_author(author_id: int, books: List[BookCreate]):
    author_info = await author.get_one_by_id(author_id)
    if not author_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    
    books_with_author_id = [_book.dict() | {"author_id": author_id} for _book in books]
    new_generated_ids = await book.create_many(books_with_author_id)
    
    created_books = []
    for new_generated_id in new_generated_ids:
        created_book = await book.get_one_by_id(new_generated_id)
        created_books.append(created_book)
    
    return created_books

@router.put("/{book_id}", response_model=BookOut, status_code=status.HTTP_201_CREATED)
async def update_book_info(book_update: BookUpdate, id: int):
    if not await book.get_one(id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await book.update(id, book_update)
    updated_book = await book.get_one(id)
    return updated_book

@router.get("/filter/", response_model=List[BookOut])
async def books_by_filters(
    skip: int = 0,
    limit: int = 10,
    title_starts_with: Optional[str] = None,
    author_name: Optional[str] = None
):
    return await book.get_many_filtered(
        skip=skip, 
        limit=limit, 
        title_starts_with=title_starts_with, 
        author_name=author_name
    )
