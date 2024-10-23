from pydantic import BaseModel, ConfigDict

class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacility(RoomFacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)