from datetime import date
from src.repositories.utils import filter_available_rooms_or_hotels
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPatch

from sqlalchemy import func, insert, select, update

class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def get_available_hotels(self, date_from: date, date_to: date):

        hotels_to_booking_get = filter_available_rooms_or_hotels(date_from, date_to)
        result = await self.session.execute(hotels_to_booking_get)

        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        
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
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
    

