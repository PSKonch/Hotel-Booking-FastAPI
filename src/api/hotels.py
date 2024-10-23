from datetime import date
from fastapi import Query, APIRouter, Body

from src.models.hotels import HotelsModel
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date | None = Query(None, description="Дата начала бронирования"),
        date_to: date | None = Query(None, description="Дата окончания бронирования"),
):
    per_page = pagination.per_page or 5

    if date_from and date_to:
        hotels_query = db.hotels.get_available_hotels(
            date_from=date_from, 
            date_to=date_to
        )
        
        if location:
            hotels_query = hotels_query.filter(HotelsModel.location.ilike(f"%{location}%"))
        
        if title:
            hotels_query = hotels_query.filter(HotelsModel.title.ilike(f"%{title}%"))
        
        result = await db.session.execute(
            hotels_query.limit(per_page).offset(per_page * (pagination.page - 1))
        )
        
        hotels = result.scalars().all()

    else:
        hotels = await db.hotels.get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )
    
    return hotels


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                }
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "ул. Шейха, 2",
                }
            }
        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
        db: DBDep,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}