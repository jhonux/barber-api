from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session

from app import crud, schemas, models, auth
from app.database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BarberAPI",
    description="API para gerenciamento de barbearia.",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- ENDPOINT DE CADASTRO DE USUÁRIO ---
@app.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    return crud.create_user(db=db, user=user)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Boas vindas ao BarberAPI!"}

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.post("/services/", response_model=schemas.Service, status_code=status.HTTP_201_CREATED)
def create_new_service(
    service: schemas.ServiceCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    
    return crud.create_service(db=db, service=service)


@app.get("/services/", response_model=List[schemas.Service])
def read_all_services(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    services = crud.get_services(db, skip=skip, limit=limit)
    return services

@app.put("/services/{service_id}", response_model=schemas.Service)
def update_existing_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_service = crud.update_service(db, service_id=service_id, service=service)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_service

@app.delete("/services/{service_id}", response_model=schemas.Service)
def delete_existing_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_service = crud.delete_service(db, service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_service

# --- ENDPOINT DE CRIAÇÃO DE DISPONIBILIDADES ---
@app.post("/availability/", response_model=schemas.Availability, status_code=status.HTTP_201_CREATED)
def create_new_availability(
    availability: schemas.AvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.create_availability(db=db, availability=availability, user_id=current_user.id)

@app.get("/availability/me/", response_model=List[schemas.Availability])
def read_my_availabilities(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_availabilities_by_user(db, user_id=current_user.id)

@app.delete("/availability/{availability_id}", response_model=schemas.Availability)
def delete_my_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_availability = crud.delete_availability(db, availability_id=availability_id, user_id=current_user.id)
    if db_availability is None:
        raise HTTPException(status_code=404, detail="Disponibilidade não encontrada")
    return db_availability

# --- ENDPOINT DE CRIAÇÃO DE AGENDAMENTOS ---
@app.post("/appointments/", response_model=schemas.Appointment, status_code=status.HTTP_201_CREATED)
def create_new_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_appointment =  crud.create_appointment(db=db, appointment=appointment, user_id=current_user.id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail=f"Serviço com id {appointment.service_id} não encontrado")
    return db_appointment

@app.get("/appointments/me/", response_model=List[schemas.Appointment])
def read_my_appointments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_appointments_by_user(db, user_id=current_user.id)

@app.delete("/appointments/{appointment_id}", response_model=schemas.Appointment)
def delete_my_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_appointment = crud.delete_appointment(db, appointment_id=appointment_id, user_id=current_user.id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return db_appointment