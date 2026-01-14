from datetime import date, time, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, schemas, models, auth
from app.models import UserRole
from app.database import SessionLocal, engine, get_db
from pydantic import BaseModel
from slugify import slugify

class AppoiontmentStatusUpdate(BaseModel):
    status: str

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BarberAPI",
    description="API para gerenciamento de barbearia.",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://trimmaapp.com.br",
    "https://www.trimmaapp.com.br",
    "https://polite-rock-0e87ed80f.1.azurestaticapps.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = auth.create_access_token(
        data={"sub": user.email,
              "role": user.role.value if user.role else "owner",
              "org_id": user.organization_id,
              "org_slug": user.organization.slug if user.organization else None
              },
        )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role.value if user.role else "owner",
        "user_name": user.name
    }


# --- ENDPOINT DE CADASTRO DE USUÁRIO ---
@app.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    base_slug = slugify(user.organization_name)
    slug = base_slug
    counter = 1
    
    while db.query(models.Organization).filter(models.Organization.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    new_org = models.Organization(
        name=user.organization_name,
        slug=slug,
        plan_type="free",
        is_active=True
    
    )
    db.add(new_org)
    db.flush()
    db.refresh(new_org)
    
    hashed_password = auth.get_password_hash(user.password)
    
    new_user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        organization_id=new_org.id,

        role=UserRole.OWNER,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


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
    
    return crud.create_service(
        db=db, 
        service=service, 
        organization_id=current_user.organization_id 
    )


@app.get("/services/", response_model=List[schemas.Service])
def read_all_services(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    services = crud.get_services_by_organization(
        db, 
        organization_id=current_user.organization_id,
        skip=skip, limit=limit)
    return services

@app.put("/services/{service_id}", response_model=schemas.Service)
def update_existing_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_service = crud.update_service(db, service_id=service_id,
                                     service=service,
                                     organization_id=current_user.organization_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_service

@app.delete("/services/{service_id}", response_model=schemas.Service)
def delete_existing_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_service = crud.delete_service(db, 
                                     organization_id=current_user.organization_id,
                                     service_id=service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return db_service


# --- ENDPOINT DE CRIAÇÃO DE BARBEIROS (USUÁRIOS) ---
@app.post("/team/", response_model=schemas.UserResponse) 
def create_team_member(
    user: schemas.UserCreateTeam, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != UserRole.OWNER and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas donos podem adicionar membros à equipe."
        )

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    hashed_password = auth.get_password_hash(user.password)
    
    new_team_member = models.User(
        email=user.email,
        hashed_password=hashed_password,
        name=user.name,
        
        organization_id=current_user.organization_id, 
        role=UserRole.BARBER, 
        is_active=True
    )
    
    db.add(new_team_member)
    db.commit()
    db.refresh(new_team_member)

    return new_team_member

@app.get("/team/", response_model=list[schemas.UserResponse])
def read_my_team(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.User)\
             .filter(models.User.organization_id == current_user.organization_id)\
             .all()

@app.delete("/team/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.role != "owner" and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas donos podem remover membros da equipe."
        )

    db_member = db.query(models.User).filter(
        models.User.id == member_id,
        models.User.organization_id == current_user.organization_id
    ).first()

    if not db_member:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    if db_member.role == "owner":
        raise HTTPException(status_code=400, detail="Não é possível remover o dono da equipe.")

    db.delete(db_member)
    db.commit()
    return None


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

@app.patch("/appointments/{appointment_id}/status", response_model=schemas.Appointment)
def update_appointment_status(
    appointment_id: int,
    status_data: AppoiontmentStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    db_appointment.status = status_data.status
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

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

@app.get("/appointments/available/", response_model=List[time])
def get_available_appointments(
    date: date,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return crud.get_available_times(db=db, user_id=current_user.id, query_date=date)