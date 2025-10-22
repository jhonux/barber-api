from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class ServiceCreate(BaseModel):
    name: str
    duration_minutes: int
    price: float


class Service(ServiceCreate):
    id: int

    class Config:
        from_attributes = True