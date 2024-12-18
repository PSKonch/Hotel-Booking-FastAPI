from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd, Facility
from src.init import redis_manager

router = APIRouter(prefix='/facilities', tags=['Удобства'])

@router.get('')
@cache(expire=1800)
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post("")
async def create_facility(db: DBDep, data: FacilityAdd):
    facility = await db.facilities.add(data)
    await db.commit()

    return facility