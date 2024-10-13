from fastapi import APIRouter, Body, Query, HTTPException, status

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import User, UserAdd, UserRequestAdd
from src.models.users import UsersModel

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

router = APIRouter(prefix='/auth', tags=['Авторизация и Аутентификация'])

@router.post('/register')
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)

    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        email_is_used = await UsersRepository(session).is_email_used(data.email)
        if email_is_used:
            return {'error': 'email is required'}
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    
    return {
        'status': 'Ok'
    }
    
