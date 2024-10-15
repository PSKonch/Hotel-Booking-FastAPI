from pydantic import BaseModel, ConfigDict
from datetime import date

class BookingRequestAdd(BaseModel):
    date_from: date
    date_to: date

class BookingAdd(BookingRequestAdd):
    user_id: int
    room_id: int
    price: int

class Booking(BookingAdd):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class BookingRequestPatch(BaseModel):
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None

class BookingPatch(BookingRequestPatch):
    room_id: int | None = None
    user_id: int | None = None

