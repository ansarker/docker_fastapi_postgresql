from pydantic import BaseModel
from datetime import date


class BorrowedByClientCreate(BaseModel):
    borrow_date: date
    return_date: date
    book_id: int
    client_id: int


class BorrowedByClientOut(BorrowedByClientCreate):
    id: int

    class Config:
        orm_mode = True