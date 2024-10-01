from pydantic import BaseModel, Field

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    name: str | None = Field(default=None)

class Hotel(BaseModel):
    title: str
    name: str