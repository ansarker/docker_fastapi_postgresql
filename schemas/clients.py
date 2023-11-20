from pydantic import BaseModel, EmailStr
from pydantic.types import constr
from typing import Optional

class ClientBase(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    sex: str
    phone: constr(
        min_length=11, max_length=14, pattern=r"(\+880)?[0-9]{11}"
    )

class ClientCreate(ClientBase):
    password: str


class ClientUpdate(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[
        constr(min_length=11, max_length=14, pattern=r"(\+880)?[0-9]{11}")
    ]
    password: Optional[str]


class ClientOut(ClientBase):
    id: int

    class Config:
        from_attributes = True


class ClientInDB(ClientBase):
    password: str