from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd, Facility

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def create_facility(db: DBDep, data: FacilityAdd):
    return await db.facilities.add(data)