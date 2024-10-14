from pydantic import BaseModel, ConfigDict

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomPatch(BaseModel):
    description: str | None
    price: int | None
    quantity: int | None