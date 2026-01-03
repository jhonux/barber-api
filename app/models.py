from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

    availabilities = relationship("Availability", back_populates="owner")
    appointments = relationship("Appointment", back_populates="barber")
    services = relationship("Service", back_populates="owner")


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    duration_minutes = Column(Integer)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    appointments = relationship("Appointment", back_populates="service")
    owner = relationship("User", back_populates="services")


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