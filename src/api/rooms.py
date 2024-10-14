from fastapi import Query, status, APIRouter, HTTPException, Body

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
        print(rooms)
        return rooms
    
@router.post('/{hotel_title}/rooms')
async def create_room(data: RoomAdd):
    async with async_session_maker() as session:
        rooms_add = await RoomsRepository(session).add(data)
        await session.commit()
    return rooms_add

@router.patch('/{hotel_title}/rooms/{room_id}')
async def partially_edit_hotel(hotel_title: str, room_id: int, data: RoomPatch):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(title=hotel_title)
        room_edit = await RoomsRepository(session).edit(data=data, exclude=True, id=room_id, hotel_id=hotel.id)
        await session.commit()
    return room_edit

@router.put('/{hotel_title}/rooms/{room_id}')
async def partially_edit_hotel(hotel_title: str, room_id: int, data: RoomPatch):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(title=hotel_title)
        room_edit = await RoomsRepository(session).edit(data=data, exclude=False, id=room_id, hotel_id=hotel.id)
        await session.commit()

@router.delete('/{hotel_title}/rooms/{room_id}')
async def delete_room(hotel_title: str, room_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(title=hotel_title)
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel.id)
        await session.commit()

    return {'status': 'ok'}