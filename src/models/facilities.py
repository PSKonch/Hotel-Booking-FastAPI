from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class FacilitiesModel(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]