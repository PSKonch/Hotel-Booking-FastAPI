from pydantic import BaseModel, EmailStr

class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str

class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr