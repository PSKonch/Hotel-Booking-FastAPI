from fastapi import APIRouter, status

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingPatch, Booking, BookingRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/bookings', tags=['Бронирование'])

@router.post('')
async def create_booking(db: DBDep, data: BookingRequestAdd, user_id: UserIdDep, room_id: int):
    room = await db.rooms.get_one_or_none(id=room_id)
    full_data = BookingAdd(room_id=room_id, user_id=user_id, **data.model_dump(), price=room.price)
    booking = await db.bookings.add(full_data)
    await db.commit()
    return {'booking': booking}

@router.get('')
async def get_all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return bookings

@router.get('/me')
async def get_my_bookings(db: DBDep, me: UserIdDep):
    bookings = await db.bookings.get_filtered(user_id=me)
    return bookings