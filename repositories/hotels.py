from repositories.base import BaseRepository
from src.models.hotels import HotelsModel

class HotelsRepository(BaseRepository):
    model = HotelsModel