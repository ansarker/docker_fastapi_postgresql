from typing import Optional, List
from sqlalchemy import select, or_, func

from schemas.books import (
    BookCreate,
    BookUpdate
)
from models import Book
from models import Author
from crud.base import CRUDBase
from utils.database import database, SessionLocal as sl


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    async def get_one_by_id(self, id: int) -> Optional[Book]:
        query = select(Book).where(Book.id == id)
        return await database.fetch_one(query)

    async def get_many_filtered(
        self,
        skip: int,
        limit: int,
        title_starts_with: str = None,
        author_name: str = None
    ) -> List[Book]:
        query = (
            select(Book)
            .join(Author)
            .where(
                Book.author_id == Author.id,
            )
            .where(
                or_(
                    func.lower(Book.title).startswith(func.lower(f"{title_starts_with}")),
                    func.lower(Author.fullname) == func.lower(f"{author_name}")
                )
            )
            .offset(skip)
            .limit(limit)
            )
        return await database.fetch_all(query)
        

book = CRUDBook(Book)