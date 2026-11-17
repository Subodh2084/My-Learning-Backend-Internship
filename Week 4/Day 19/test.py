import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from jose import jwt
from app.main import app, create_access_token, SECRET_KEY, ALGORITHM

client = TestClient(app)

def test_login_success():
    """Verify standard valid login lifecycle."""
    response = client.post(
        "/login",
        data={"username": "developer@example.com", "password": "supersecurepassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Inspect payload layout to ensure no secrets leaked
    payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert "hashed_password" not in payload
    assert payload["sub"] == "developer@example.com"

def test_login_invalid_password():
    """Verify invalid passwords are explicitly rejected."""
    response = client.post(
        "/login",
        data={"username": "developer@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_missing_token():
    """Verify protected endpoints reject requests missing authorization headers."""
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_tampered_token():
    """Verify token validation fails if payload/signature is modified."""
    # 1. Get valid token
    response = client.post(
        "/login",
        data={"username": "developer@example.com", "password": "supersecurepassword123"}
    )
    valid_token = response.json()["access_token"]
    
    # 2. Break the signature block manually
    tampered_token = valid_token[:-5] + "XXXXX"
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {tampered_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_expired_token():
    """Verify expired standard claims result in an unauthorized classification."""
    # Create a token backdated past its expiration threshold
    expired_token = create_access_token(
        data={"sub": "developer@example.com"},
        expires_delta=timedelta(minutes=-5)
    )
    
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
