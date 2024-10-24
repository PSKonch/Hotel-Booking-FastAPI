from datetime import date
from sqlalchemy import insert, select, func
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.repositories.utils import filter_available_rooms_or_hotels
from src.models.rooms import RoomsModel
from src.schemas.rooms import Room, RoomAdd, RoomWithRelations
from src.models.bookings import BookingsModel
from src.database import engine

class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = RoomWithRelations


    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
            .options(selectinload(RoomsModel.facilities))
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    
    async def get_available_rooms(self, hotel_id, date_from: date, date_to: date):
        
        rooms_to_booking_get = filter_available_rooms_or_hotels(date_from, date_to, hotel_id)
        result = await self.session.execute(rooms_to_booking_get)

        return [self.schema.model_validate(model) for model in result.scalars().all()]
    




