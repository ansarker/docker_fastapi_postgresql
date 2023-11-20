from typing import Optional
from sqlalchemy import select

from schemas import AuthorCreate, AuthorUpdate
from models import Author
from .base import CRUDBase
from utils.database import database


class CRUDClient(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    async def get_one_by_id(self, id: int) -> Optional[Author]:
        query = select(Author).where(Author.id == id)
        return await database.fetch_one(query)

author = CRUDClient(Author)