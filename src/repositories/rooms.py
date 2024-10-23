from datetime import date
from sqlalchemy import insert, select, func

from src.repositories.base import BaseRepository
from src.repositories.utils import filter_available_rooms_or_hotels
from src.models.rooms import RoomsModel
from src.schemas.rooms import Room, RoomAdd
from src.models.bookings import BookingsModel
from src.database import engine

class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_available_rooms(self, hotel_id, date_from: date, date_to: date):
        
        rooms_to_booking_get = filter_available_rooms_or_hotels(date_from, date_to, hotel_id)
        result = await self.session.execute(rooms_to_booking_get)

        return [self.schema.model_validate(model) for model in result.scalars().all()]
    




