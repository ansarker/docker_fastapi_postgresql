from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from sqlalchemy.sql import select, delete, update, insert

from utils.database import database

Base = declarative_base()

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_one(self, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        return await database.fetch_one(query)

    async def get_many(self, skip: int, limit: int) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        return await database.fetch_all(query)

    async def create(self, object_in: CreateSchemaType) -> int:
        query = insert(self.model).values(**object_in.dict())
        return await database.execute(query)
    
    async def create_many(self, objects_in: List[CreateSchemaType]) -> List[int]:
        new_generated_ids = []
        for obj_in in objects_in:
            query = insert(self.model).values(**obj_in)
            new_generated_id = await database.execute(query)
            new_generated_ids.append(new_generated_id)
        return new_generated_ids

    async def update(self, id: int, payload: UpdateSchemaType) -> None:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**payload.dict(exclude_unset=True))
        )
        await database.execute(query)

    async def remove(self, id: int) -> None:
        query = delete(self.model).where(self.model.id == id)
        await database.execute(query)