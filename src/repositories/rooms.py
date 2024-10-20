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
        rooms_count = (
            select(BookingsModel.room_id, func.count("*").label('rooms_booked'))
            .select_from(BookingsModel)
            .filter(
                    BookingsModel.date_from <= date_from, 
                    BookingsModel.date_to >= date_to
                    )
            .group_by(BookingsModel.room_id)
            .cte(name='rooms_count')
            )
        rooms_left_table = (
            select(
                RoomsModel.id.label('rooms_id'), 
                (RoomsModel.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label('rooms_left')
                )
            .select_from(RoomsModel)
            .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
            .cte(name='rooms_left_table')
            )   
            
        query = (select(rooms_left_table)
        .select_from(rooms_left_table)
        .filter(rooms_left_table.c.rooms_left > 0))




