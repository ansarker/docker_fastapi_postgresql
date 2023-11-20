from pydantic import BaseModel
from datetime import datetime

class AuthorBase(BaseModel):
    fullname: str

    class Config:
        from_attributes = True

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    fullname: str

class AuthorDB(AuthorBase):
    id: int
    created_at: datetime

class AuthorOut(AuthorCreate):
    id: int