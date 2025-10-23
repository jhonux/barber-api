from sqlalchemy.orm import Session
from app import models, schemas, auth



def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)

    db_user = models.User(email=user.email, hashed_password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()

def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(
        name=service.name,
        duration_minutes=service.duration_minutes,
        price=service.price
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def update_service(db: Session, service_id: int, service: schemas.ServiceUpdate):
    db_service = get_service_by_id(db, service_id)
    if db_service:
        update_data = service.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_service, key, value)
        db.commit()
        db.refresh(db_service)
    return db_service

def delete_service(db: Session, service_id: int):
    db_service = get_service_by_id(db, service_id)
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service


# --- CRUD DE DISPONIBILIDADES ---

def create_availability(db: Session, availability: schemas.AvailabilityCreate, user_id: int):
    db_availability = models.Availability(
        **availability.dict(),
        user_id=user_id
    )
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability

def get_availabilities_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Availability).filter(
        models.Availability.user_id == user_id
    ).offset(skip).limit(limit).all()

def delete_availability(db: Session, availability_id: int, user_id: int):
    db_availability = db.query(models.Availability).filter(
        models.Availability.id == availability_id,
        models.Availability.user_id == user_id
    ).first()

    if db_availability:
        db.delete(db_availability)
        db.commit()
    return db_availability

# --- CRUD DE AGENDAMENTOS (APPOINTMENTS) ---
def create_appointment(db: Session, appointment: schemas.AppointmentCreate, user_id: int):
    db_appointment = models.Appointment(
        **appointment.dict(),
        user_id=user_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

def get_appointments_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).filter(
        models.Appointment.user_id == user_id
    ).offset(skip).limit(limit).all()

def delete_appointment(db: Session, appointment_id: int, user_id: int):
    db_appointment = db.query(models.Appointment).filter(
        models.Appointment.id == appointment_id,
        models.Appointment.user_id == user_id
    ).first()

    if db_appointment:
        db.delete(db_appointment)
        db.commit()
    return db_appointment