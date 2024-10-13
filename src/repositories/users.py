from sqlalchemy import select, Boolean

from src.repositories.base import BaseRepository

from src.models.users import UsersModel
from src.schemas.users import User, UserAdd

class UsersRepository(BaseRepository):
    model = UsersModel  
    schema = User

    async def is_email_used(self, email: str) -> bool:
        query = select(self.model).where(self.model.email==email)
        result = await self.session.execute(query)
        response = result.scalars().first()
        return response is not None
        