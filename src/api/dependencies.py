from typing import Annotated

from fastapi import Depends, Query, Request, HTTPException, status
from pydantic import BaseModel

from src.utils.db_manager import DBManager
from src.services.auth import AuthService
from src.database import async_session_maker


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request):
    access_token = request.cookies.get('access_token', None)
    if not access_token:
        raise HTTPException(status_code=401, detail='Вы не аутентифицированы')
    return access_token

def get_current_user_id(token: Annotated[str, Depends(get_token)]) -> int:
    decoded_token = AuthService().decode_token(token)
    return decoded_token['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]

def get_db_manager():
    return


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]