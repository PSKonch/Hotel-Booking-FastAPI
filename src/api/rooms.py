from datetime import date
from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.schemas.rooms_facilities import RoomFacilityAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_available_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_available_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/all")
async def get_rooms_by_hotel(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities = [RoomFacilityAdd(room_id=room.id, facility_id=facility_id_) for facility_id_ in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities)

    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.edit(_room_data, id=room_id)
    
    existing_facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    existing_facilities_ids = {facility.facility_id for facility in existing_facilities}

    new_facility_ids = set(room_data.facilities_ids or [])

    facilities_to_remove = existing_facilities_ids - new_facility_ids

    facilities_to_add = new_facility_ids - existing_facilities_ids

    if facilities_to_remove:
        await db.rooms_facilities.remove_bulk([
            facility.id for facility in existing_facilities if facility.facility_id in facilities_to_remove
        ])

    if facilities_to_add:
        rooms_facilities_to_add = [
            RoomFacilityAdd(room_id=room_id, facility_id=facility_id_) 
            for facility_id_ in facilities_to_add
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_to_add)

    await db.commit()
    return {'status': 'ok'}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    room = await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

    existing_facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    existing_facilities_ids = {facility.facility_id for facility in existing_facilities}

    new_facility_ids = set(room_data.facilities_ids or [])

    facilities_to_remove = existing_facilities_ids - new_facility_ids

    facilities_to_add = new_facility_ids - existing_facilities_ids

    if facilities_to_remove:
        await db.rooms_facilities.remove_bulk([
            facility.id for facility in existing_facilities if facility.facility_id in facilities_to_remove
        ])

    if facilities_to_add:
        rooms_facilities_to_add = [
            RoomFacilityAdd(room_id=room_id, facility_id=facility_id_) 
            for facility_id_ in facilities_to_add
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_to_add)

    await db.commit()
    return {'status': 'ok'}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}