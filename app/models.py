from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, Date

from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    duration_minutes = Column(Integer)
    price = Column(Float)


class Availabilty(Base):
    __tablename__ = "availabilities"
    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer)
    start_time = Column(Time)
    end_time = Column(Time)
    user_id = Column(Integer, ForeignKey("users.id"))


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(100))
    client_email = Column(String(100))
    Appointment_date = Column(Date)
    Appointment_time = Column(Time)
    service_id = Column(Integer, ForeignKey("services.id"))