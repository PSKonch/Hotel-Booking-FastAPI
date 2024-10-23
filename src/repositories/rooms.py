from datetime import date
from sqlalchemy import insert, select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsModel
from src.schemas.rooms import Room, RoomAdd
from src.models.bookings import BookingsModel
from src.database import engine

class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        
        booked_rooms = (select(BookingsModel.room_id)
                        .select_from(BookingsModel)
                        .filter(BookingsModel.date_from <= date_from, BookingsModel.date_to >= date_to)
                        .subquery('booked_rooms'))
        
        available_rooms = (select(RoomsModel)
                           .filter(RoomsModel.id.not_in(booked_rooms))
                           .filter(RoomsModel.hotel_id == hotel_id))

        result = await self.session.execute(available_rooms)

        return [self.schema.model_validate(model) for model in result.scalars().all()]
    




