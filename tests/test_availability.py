from fastapi.testclient import TestClient
from app.main import app 
test_avail_user_email = "avail_test@example.com"
test_avail_user_password = "password123"

# --- Função Auxiliar para Autenticação ---

def get_auth_headers(client: TestClient) -> dict:
    """Cria um utilizador (se necessário) e obtém um token de acesso."""
    client.post("/users/", json={"email": test_avail_user_email, "password": test_avail_user_password})
    login_response = client.post(
        "/token",
        data={"username": test_avail_user_email, "password": test_avail_user_password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]
    return {"Authorization": f"Bearer {access_token}"}

# --- Testes do CRUD de Disponibilidade ---

created_availability_id = None

def test_create_availability_success(client: TestClient):
    """Testa a criação de um horário de disponibilidade (requer auth)."""
    global created_availability_id
    headers = get_auth_headers(client)

    response = client.post(
        "/availability/",
        headers=headers,
        json={"day_of_week": 2, "start_time": "09:00:00", "end_time": "18:00:00"}, 
    )
    assert response.status_code == 201
    data = response.json()
    assert data["day_of_week"] == 2
    assert data["start_time"] == "09:00:00"
    assert "id" in data
    assert "user_id" in data
    created_availability_id = data["id"]

def test_create_availability_unauthenticated(client: TestClient):
    """Testa a criação sem autenticação."""
    response = client.post(
        "/availability/",
        json={"day_of_week": 3, "start_time": "10:00:00", "end_time": "17:00:00"},
    )
    assert response.status_code == 401

def test_read_my_availabilities_success(client: TestClient):
    """Testa a listagem das próprias disponibilidades (requer auth)."""
    headers = get_auth_headers(client)
    response = client.get("/availability/me/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(avail["id"] == created_availability_id for avail in data)

def test_read_my_availabilities_unauthenticated(client: TestClient):
    """Testa a listagem sem autenticação."""
    response = client.get("/availability/me/")
    assert response.status_code == 401

def test_delete_my_availability_success(client: TestClient):
    """Testa a remoção de uma disponibilidade (requer auth)."""
    assert created_availability_id is not None
    headers = get_auth_headers(client)

    response = client.delete(f"/availability/{created_availability_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_availability_id

  
    response_get = client.get("/availability/me/", headers=headers)
    assert response_get.status_code == 200
    assert not any(avail["id"] == created_availability_id for avail in response_get.json())

def test_delete_availability_not_found(client: TestClient):
    """Testa a remoção de uma disponibilidade que não existe."""
    headers = get_auth_headers(client)
    response = client.delete("/availability/99999", headers=headers)
    assert response.status_code == 404