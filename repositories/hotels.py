from repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPATCH

from sqlalchemy import func, insert, select, update

class HotelsRepository(BaseRepository):
    model = HotelsModel

    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    

