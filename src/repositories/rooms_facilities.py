from sqlalchemy import delete, insert, select


from src.repositories.base import BaseRepository
from src.schemas.rooms_facilities import RoomFacility, RoomFacilityAdd
from src.models.rooms_facilities import RoomsFacilitiesModel


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility

    async def remove_bulk(self, room_id: int, facility_ids: list[int]):
        stmt = delete(self.model).where(
            self.model.room_id == room_id,
            self.model.facility_id.in_(facility_ids)
        )
        await self.session.execute(stmt)

    async def add_bulk(self, room_id: int, facility_ids: list[int]):
        new_facilities = [
            RoomFacilityAdd(room_id=room_id, facility_id=facility_id) 
            for facility_id in facility_ids
        ]
        
        stmt = insert(self.model).values([item.model_dump() for item in new_facilities])
        
        await self.session.execute(stmt)


    async def update_room_facilities(self, room_id: int, facilities_ids: list[int]):

        query = select(RoomsFacilitiesModel.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        current_facilities_ids: list[int] = result.scalars().all()

        delete_facilities_ids = set(current_facilities_ids) - set(facilities_ids)
        add_facilities_ids = set(facilities_ids) - set(current_facilities_ids)

        if delete_facilities_ids:
            await self.remove_bulk(room_id=room_id, facility_ids=list(delete_facilities_ids))

        if add_facilities_ids:
            await self.add_bulk(room_id=room_id, facility_ids=list(add_facilities_ids))



        