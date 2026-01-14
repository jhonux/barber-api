import enum
from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Date, DateTime, Boolean, Enum as PgEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class UserRole(str, enum.Enum):
    OWNER = "owner"
    BARBER = "barber"
    ADMIN = "admin"
    

from app.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True)
    segment = Column(String, default="barbershop")
    plan_type = Column(String, default="beta")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    users = relationship("User", back_populates="organization")


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String(255))

    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", back_populates="users")
    role = Column(PgEnum(UserRole), default=UserRole.OWNER, nullable=False, server_default='OWNER')
    
    availabilities = relationship("Availability", back_populates="owner")
    appointments = relationship("Appointment", back_populates="barber")


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    duration_minutes = Column(Integer)
    price = Column(Float)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    appointments = relationship("Appointment", back_populates="service")


class Availability(Base):
    __tablename__ = "availabilities"
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)
    start_time = Column(Time)
    end_time = Column(Time)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="availabilities")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100))
    client_email = Column(String(100))
    client_phone = Column(String(20), nullable=True)
    appointment_date = Column(Date)
    appointment_time = Column(Time)
    service_id = Column(Integer, ForeignKey("services.id"))
    
    status = Column(String, default="pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    barber = relationship("User", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")