from fastapi.testclient import TestClient
from app.main import app

test_user_email = "teste@examp.com"
test_user_password = "senha123"

# Teste de cadastro
def test_create_user_success(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "email": test_user_email,
            "password": test_user_password
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert response.json()
    assert "id" in data

    assert "hashed_password" not in data

def test_create_user_duplicate_email(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "email": test_user_email,
            "password": "anotherpassword"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "E-mail já cadastrado"}

# Teste de login
def test_login_success(client: TestClient):
    """Testa o login com credenciais corretas."""
    response = client.post(
        "/token",
        data={"username": test_user_email, "password": test_user_password} 
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    """Testa o login com a palavra-passe errada."""
    response = client.post(
        "/token",
        data={"username": test_user_email, "password": "wrongpassword"}
    )
    assert response.status_code == 401 
    assert response.json() == {"detail": "E-mail ou senha incorretos"}

def test_login_nonexistent_user(client: TestClient):
    """Testa o login com um e-mail que não existe."""
    response = client.post(
        "/token",
        data={"username": "nonexistent@example.com", "password": "password123"}
    )
    assert response.status_code == 401 
    assert response.json() == {"detail": "E-mail ou senha incorretos"}