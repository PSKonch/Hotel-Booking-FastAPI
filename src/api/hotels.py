from fastapi import Query, APIRouter, Body, status

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.repositories.hotels import HotelsRepository


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description='Адрес')
):

    limit = pagination.per_page or 5
    offset = pagination.page * (pagination.page - 1)
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=limit,
            offset=offset
        )

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]


@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int):

    async with async_session_maker() as session:
        hotels_repository = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        await session.commit()

    return hotels_repository

@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotels_repository = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return hotels_repository


@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        hotels_repository = await HotelsRepository(session).edit(hotel_data, exclude=False, id=hotel_id)
        await session.commit()
    
    return {
        'status': 'was updated'
    }   


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
):
    async with async_session_maker() as session:
        hotels_repository = await HotelsRepository(session).edit(data=hotel_data, exclude=True, id=hotel_id)
        await session.commit()

    return {
        'status': 'ok'
    }

@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

    return {
        'status': 'Ok',
        'description': 'hotes was deleted'
    }