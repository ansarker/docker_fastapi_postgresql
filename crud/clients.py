from typing import Optional
from sqlalchemy import select

from schemas.clients import ClientCreate, ClientUpdate
from models import Client
from .base import CRUDBase
from utils.database import database


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    async def get_one_by_email(self, email: str) -> Optional[Client]:
        query = select(Client).where(Client.email == email)
        return await database.fetch_one(query)

    async def get_one_by_username(self, username: str) -> Optional[Client]:
        query = select(Client).where(Client.username == username)
        return await database.fetch_one(query)

client = CRUDClient(Client)