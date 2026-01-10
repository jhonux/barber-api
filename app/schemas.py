from datetime import time, date
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    password: str
    organization_name: str    

class UserCreateTeam(UserBase):
    name: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str      
    is_active: bool
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_name: str


class ServiceBase(BaseModel):
    name: str
    duration_minutes: int
    price: float

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None

class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True

class AvailabilityBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time

class AvailabilityCreate(AvailabilityBase):
    
    @field_validator('day_of_week')
    @classmethod
    def validate_day_of_week(cls, v: int) -> int:
        return (v + 6) % 7


class Availability(AvailabilityBase):
    id: int
    user_id: int
    
    @field_validator('day_of_week', mode='before')
    @classmethod
    def validate_day_of_week(cls, v: int) -> int:
        return (v + 1) % 7

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    client_name: str
    client_email: EmailStr
    client_phone: Optional[str] = None
    appointment_date: date
    appointment_time: time
    service_id: int

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    user_id: int
    
    status: Optional[str] = "pending"

    class Config:
        from_attributes = True


