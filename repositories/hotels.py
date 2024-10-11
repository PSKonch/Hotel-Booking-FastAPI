from repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel

from sqlalchemy import func, insert, select

class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsModel)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def add(self, data: Hotel):
        stmt = insert(HotelsModel).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()