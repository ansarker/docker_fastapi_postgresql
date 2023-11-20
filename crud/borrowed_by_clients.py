from datetime import date
from sqlalchemy import select, or_, and_
from typing import List

from .base import CRUDBase
from models import BorrowedByClient
from schemas.borrowed_by_clients import BorrowedByClientCreate
from utils.database import database


class CRUDBorrowedByClient(CRUDBase[BorrowedByClient, BorrowedByClientCreate, None]):
    async def get_many_by_borrowed_date(
        self, borrow_date: date, return_date: date, book_id: int
    ) -> List[BorrowedByClient]:
        query = (
            select(BorrowedByClient)
            .where(BorrowedByClient.book_id == book_id)
            .where(
                or_(
                    BorrowedByClient.borrow_date.between(borrow_date, return_date),
                    BorrowedByClient.return_date.between(borrow_date, return_date),
                )
            )
        )

        return await database.fetch_all(query)

    async def get_many_filtered_by_client_id(self, client_id: int) -> List[BorrowedByClient]:
        query = select(BorrowedByClient).where(
            and_(
                BorrowedByClient.client_id == client_id,
            )
        )
        return await database.fetch_all(query)


borrowed_by_client = CRUDBorrowedByClient(BorrowedByClient)