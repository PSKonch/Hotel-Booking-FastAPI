from src.repositories.base import BaseRepository
from src.schemas.rooms_facilities import RoomFacility
from src.models.rooms_facilities import RoomsFacilitiesModel

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility