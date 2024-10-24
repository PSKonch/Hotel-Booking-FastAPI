from datetime import date
from src.repositories.utils import filter_available_rooms_or_hotels
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPatch
from src.repositories.mappers.mappers import HotelDataMapper

from sqlalchemy import func, insert, select, update

class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self, 
        date_from: date, 
        date_to: date, 
        location: str | None = None, 
        title: str | None = None, 
        limit: int | None = None, 
        offset: int | None = None
    ) -> list[Hotel]:
        
        hotels_query = filter_available_rooms_or_hotels(date_from, date_to)

        if location:
            hotels_query = hotels_query.filter(func.lower(HotelsModel.location).contains(location.strip().lower())) 
        if title:
            hotels_query = hotels_query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))

        hotels_query = hotels_query.limit(limit).offset(offset)
        result = await self.session.execute(hotels_query)
        
        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
    

