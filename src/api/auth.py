from typing import Annotated

from fastapi import APIRouter, Body, Query, HTTPException, status, Response, Depends, Request

from passlib.context import CryptContext

import jwt
from pydantic import EmailStr

from src.database import async_session_maker
from src.services.auth import AuthService
from src.repositories.users import UsersRepository
from src.schemas.users import User, UserAdd, UserRequestAdd
from src.models.users import UsersModel
from src.api.dependencies import UserIdDep, get_token

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
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не существует')
        
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный пароль')
        
        access_token = AuthService().create_access_token(({'user_id': user.id}))
        response.set_cookie('access_token', access_token)

        return {'access_toket': access_token}

@router.get('/me')
async def get_me(user_id: UserIdDep): 
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user

@router.post('/logout')
async def logout(response: Response):
    response.set_cookie('access_token', '')
    return {'status': 'Ok'}


