from typing import List
from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException

from schemas.borrowed_by_clients import BorrowedByClientCreate, BorrowedByClientOut
from models import Client
from api.dependencies import get_current_user
from crud.borrowed_by_clients import borrowed_by_client

router = APIRouter()


@router.post("/", response_model=BorrowedByClientOut, status_code=status.HTTP_201_CREATED)
async def borrow_a_book(
    bbc_in: BorrowedByClientCreate,
    current_client: Client = Depends(get_current_user),
):
    booked_by_user_info = await borrowed_by_client.get_many_by_borrowed_date(
        bbc_in.borrow_date, bbc_in.return_date, bbc_in.book_id
    )
    if booked_by_user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to borrow book in between these dates",
        )
    new_generated_id = await borrowed_by_client.create(bbc_in)
    return {**bbc_in.dict(), "id": new_generated_id}


@router.delete("/{bbc_id}", status_code=status.HTTP_202_ACCEPTED)
async def remove_booking(
    bbc_id: int, current_client: Client = Depends(get_current_user)
):
    if not await borrowed_by_client.get_one(bbc_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    await borrowed_by_client.remove(bbc_id)
    return {"message": "deleted successfully"}

@router.get("/client_id", response_model=List[BorrowedByClientOut], status_code=status.HTTP_200_OK)
async def borrow_by_client(client_id: int, borrowed_by=BorrowedByClientOut):
    borrowed = await borrowed_by_client.get_many_filtered_by_client_id(client_id=client_id)
    return [BorrowedByClientOut(**bor).dict() for bor in borrowed]