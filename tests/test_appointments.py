import pytest 
from fastapi.testclient import TestClient
from app.main import app 
from datetime import date, time

# --- Dados de Teste ---
test_appt_user_email = "appt_test@example.com"
test_appt_user_password = "password123"
valid_service_id = None 

# --- Função Auxiliar para Autenticação ---

def get_auth_headers(client: TestClient) -> dict:
    """Cria um utilizador (se necessário) e obtém um token de acesso."""
    client.post("/users/", json={"email": test_appt_user_email, "password": test_appt_user_password})
    login_response = client.post(
        "/token",
        data={"username": test_appt_user_email, "password": test_appt_user_password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

# --- Função Auxiliar para Criar um Serviço ---

def create_test_service(client: TestClient, headers: dict) -> int:
    """Cria um serviço de teste e retorna o seu ID."""
    global valid_service_id
    if valid_service_id: 
         return valid_service_id

    response = client.post(
        "/services/",
        headers=headers,
        json={"name": "Serviço de Teste Appt", "duration_minutes": 60, "price": 100.0}
    )
    if response.status_code != 201:
         pytest.skip("Não foi possível criar o serviço necessário para os testes de agendamento.")
    valid_service_id = response.json()["id"]
    return valid_service_id

# --- Testes do CRUD de Agendamentos ---

created_appointment_id = None

def test_create_appointment_success(client: TestClient):
    """Testa a criação de um agendamento manual (requer auth)."""
    global created_appointment_id
    headers = get_auth_headers(client)
    service_id = create_test_service(client, headers) 

    test_date = date.today().isoformat() 
    test_time = "14:00:00"

    response = client.post(
        "/appointments/",
        headers=headers,
        json={
            "client_name": "Cliente Teste Appt", 
            "client_email": "cliente@appt.com", 
            "appointment_date": test_date, 
            "appointment_time": test_time, 
            "service_id": service_id
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["client_name"] == "Cliente Teste Appt"
    assert data["appointment_date"] == test_date
    assert data["service_id"] == service_id
    assert "id" in data
    assert "user_id" in data
    created_appointment_id = data["id"]

def test_create_appointment_unauthenticated(client: TestClient):
    """Testa a criação sem autenticação."""
    response = client.post(
        "/appointments/",
        json={
            "client_name": "Cliente Fantasma", 
            "client_email": "fantasma@appt.com", 
            "appointment_date": date.today().isoformat(), 
            "appointment_time": "15:00:00", 
            "service_id": 999 
        },
    )
    assert response.status_code == 401

def test_create_appointment_invalid_service(client: TestClient):
    """Testa a criação com um service_id inválido (requer auth)."""
    headers = get_auth_headers(client)
    response = client.post(
        "/appointments/",
        headers=headers,
        json={
            "client_name": "Cliente Erro", 
            "client_email": "erro@appt.com", 
            "appointment_date": date.today().isoformat(), 
            "appointment_time": "16:00:00", 
            "service_id": 99999 
        },
    )
    assert response.status_code == 404

def test_read_my_appointments_success(client: TestClient):
    """Testa a listagem dos próprios agendamentos (requer auth)."""
    headers = get_auth_headers(client)
    response = client.get("/appointments/me/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(appt["id"] == created_appointment_id for appt in data if created_appointment_id)

def test_read_my_appointments_unauthenticated(client: TestClient):
    """Testa a listagem sem autenticação."""
    response = client.get("/appointments/me/")
    assert response.status_code == 401

def test_delete_my_appointment_success(client: TestClient):
    """Testa a remoção de um agendamento (requer auth)."""
    if not created_appointment_id: 
         pytest.skip("ID do agendamento não disponível para teste de remoção.")

    headers = get_auth_headers(client)

    response = client.delete(f"/appointments/{created_appointment_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_appointment_id

   
    response_get = client.get("/appointments/me/", headers=headers)
    assert response_get.status_code == 200
    assert not any(appt["id"] == created_appointment_id for appt in response_get.json())

def test_delete_appointment_not_found(client: TestClient):
    """Testa a remoção de um agendamento que não existe."""
    headers = get_auth_headers(client)
    response = client.delete("/appointments/99999", headers=headers)
    assert response.status_code == 404