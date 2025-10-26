
from fastapi.testclient import TestClient
from app.main import app 
test_user_email = "service_test@example.com"
test_user_password = "password123"

# --- Função Auxiliar para Autenticação ---

def get_auth_headers(client: TestClient) -> dict:
    """Cria um utilizador (se necessário) e obtém um token de acesso."""
    client.post("/users/", json={"email": test_user_email, "password": test_user_password})

    login_response = client.post(
        "/token",
        data={"username": test_user_email, "password": test_user_password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    return {"Authorization": f"Bearer {access_token}"}

# --- Testes do CRUD de Serviços ---

created_service_id = None 

def test_create_service_success(client: TestClient):
    """Testa a criação de um novo serviço com sucesso (requer auth)."""
    global created_service_id
    headers = get_auth_headers(client)

    response = client.post(
        "/services/",
        headers=headers, 
        json={"name": "Corte Teste", "duration_minutes": 30, "price": 50.0},
    )
    assert response.status_code == 201 
    data = response.json()
    assert data["name"] == "Corte Teste"
    assert data["price"] == 50.0
    assert "id" in data
    created_service_id = data["id"] 

def test_create_service_unauthenticated(client: TestClient):
    """Testa se a API impede a criação sem autenticação."""
    response = client.post(
        "/services/", 
        json={"name": "Corte Pirata", "duration_minutes": 10, "price": 5.0},
    )
    assert response.status_code == 401 

def test_read_services_success(client: TestClient):
    """Testa a listagem de serviços com sucesso (requer auth)."""
    headers = get_auth_headers(client)
    response = client.get("/services/", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) 
    assert any(service["id"] == created_service_id and service["name"] == "Corte Teste" for service in data)

def test_read_services_unauthenticated(client: TestClient):
    """Testa se a API impede a listagem sem autenticação."""
    response = client.get("/services/") 
    assert response.status_code == 401

def test_update_service_success(client: TestClient):
    """Testa a atualização de um serviço com sucesso (requer auth)."""
    assert created_service_id is not None 
    headers = get_auth_headers(client)

    response = client.put(
        f"/services/{created_service_id}",
        headers=headers,
        json={"price": 60.0, "duration_minutes": 35} 
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_service_id
    assert data["price"] == 60.0
    assert data["duration_minutes"] == 35
    assert data["name"] == "Corte Teste" 

def test_update_service_not_found(client: TestClient):
    """Testa a atualização de um serviço que não existe."""
    headers = get_auth_headers(client)
    response = client.put(
        "/services/99999", 
        headers=headers,
        json={"price": 100.0}
    )
    assert response.status_code == 404 

def test_delete_service_success(client: TestClient):
    """Testa a remoção de um serviço com sucesso (requer auth)."""
    assert created_service_id is not None
    headers = get_auth_headers(client)

    response = client.delete(f"/services/{created_service_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_service_id 

   
    response_get = client.get(f"/services/", headers=headers) 
    assert response_get.status_code == 200
    assert not any(service["id"] == created_service_id for service in response_get.json())

def test_delete_service_not_found(client: TestClient):
    """Testa a remoção de um serviço que não existe."""
    headers = get_auth_headers(client)
    response = client.delete("/services/99999", headers=headers)
    assert response.status_code == 404