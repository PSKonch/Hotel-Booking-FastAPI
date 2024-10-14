from fastapi import status, APIRouter, HTTPException, Body

from src.database import async_session_maker
from src.schemas.rooms import Room, RoomAdd, RoomPatch
from src.repositories.rooms import RoomsRepository
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix='/hotels', tags=['Номера'])

@router.get('/{hotel_title}/rooms')
async def get_rooms(hotel_title: str):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(title=hotel_title)
        rooms = await RoomsRepository(session).get_all(hotel_id=hotel.id)
        return rooms
    
@router.post('/rooms')
async def create_room(data: RoomAdd):
    async with async_session_maker() as session:
        rooms_add = await RoomsRepository(session).add(data)
        await session.commit()
    return rooms_add