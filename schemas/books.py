from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BookBase(BaseModel):
    title: str
    year: int
    publisher: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    year: Optional[int]
    publisher: Optional[str]
    author_id: Optional[int] = None

class BookOut(BaseModel):
    id: int
    title: str
    year: int
    publisher: str
    author_id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True