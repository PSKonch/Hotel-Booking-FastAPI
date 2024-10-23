from datetime import date
from sqlalchemy import and_, insert, or_, select, func

from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.models.bookings import BookingsModel


def filter_available_rooms_or_hotels(date_from: date, date_to: date, hotel_id: int = None):
    booked_rooms = (
        select(BookingsModel.room_id)
        .select_from(BookingsModel)
        .filter(
            or_(
                and_(BookingsModel.date_from <= date_to, BookingsModel.date_to >= date_from)
            )
        )
        .subquery('booked_rooms')
    )
    
    if hotel_id:
        available_rooms = (
            select(RoomsModel)
            .filter(RoomsModel.id.not_in(booked_rooms))
            .filter(RoomsModel.hotel_id == hotel_id)
        )
        return available_rooms
    else:
        available_hotels = (
            select(HotelsModel)
            .join(RoomsModel, RoomsModel.hotel_id == HotelsModel.id)
            .filter(RoomsModel.id.not_in(booked_rooms))
            .distinct()
        )
        return available_hotels