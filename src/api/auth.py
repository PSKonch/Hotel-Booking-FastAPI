from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Body, Query, HTTPException, status, Response

from passlib.context import CryptContext

import jwt

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import User, UserAdd, UserRequestAdd
from src.models.users import UsersModel

SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/register')
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)

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
        
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверный пароль')
        
        access_token = create_access_token({'user_id': user.id})
        resonse.set_cookie('access_token', access_token)

        return {'access_toket': access_token}
