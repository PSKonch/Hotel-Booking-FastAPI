from fastapi import APIRouter, status

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingPatch, Booking, BookingRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/bookings', tags=['Бронирование'])

@router.post('')
async def create_booking(db: DBDep, data: BookingRequestAdd, user_id: UserIdDep):
    full_data = BookingAdd(user_id=user_id, **data.model_dump())
    booking = await db.bookings.add(full_data)
    await db.commit()
    return {'booking': booking}