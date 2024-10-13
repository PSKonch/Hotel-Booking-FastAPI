from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Body, Query, HTTPException, status, Response, Request

from passlib.context import CryptContext

import jwt
from pydantic import EmailStr

from src.database import async_session_maker
from src.services.auth import AuthService
from src.repositories.users import UsersRepository
from src.schemas.users import User, UserAdd, UserRequestAdd
from src.models.users import UsersModel

router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])

@router.post('/register')
async def register_user(data: UserRequestAdd):
    hashed_password = AuthService().hash_password(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    
    return {
        'status': 'Ok'
    }

@router.post('/login')
async def login_user(data: UserRequestAdd, resonse: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не существует')
        
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный пароль')
        
        access_token = AuthService().create_access_token(({'user_id': user.id}))
        resonse.set_cookie('access_token', access_token)

        return {'access_toket': access_token}

@router.get('/only_auth')
async def only_auth(request: Request, email: EmailStr): 
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=email)

        if not user:
            return {'token': None}
        
        access_token = request.cookies.get('access_token')

        return {'token': access_token}

