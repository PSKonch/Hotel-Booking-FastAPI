from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

class FacilitiesModel(Base):
    __tablename__ = 'facilities'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    rooms: Mapped[list['RoomsModel']] = relationship( # type: ignore
        back_populates='facilities',
        secondary='rooms_facilities'
    )