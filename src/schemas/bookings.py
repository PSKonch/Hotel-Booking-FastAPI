from pydantic import BaseModel, ConfigDict
from datetime import date

class BookingRequestAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    price: int

class BookingAdd(BookingRequestAdd):
    user_id: int

class Booking(BookingAdd):
    id: int
    user_id: int

class BookingRequestPatch(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None

class BookingPatch(BookingRequestPatch):
    room_id: int | None = None
    user_id: int | None = None

