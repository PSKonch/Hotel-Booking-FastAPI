from pydantic import BaseModel, ConfigDict

class FacilityAdd(BaseModel):
    title: str

class Facility(FacilityAdd):
    id: int