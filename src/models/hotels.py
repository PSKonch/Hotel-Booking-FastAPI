from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

from src.database import Base



class HotelsModel(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=100), unique=True)
    location: Mapped[str]