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