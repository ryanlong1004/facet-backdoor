import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "openapi" in response.text.lower()


def test_login_invalid():
    response = client.post(
        "/token/login",
        data={"username": "wrong", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.text


# Add more endpoint tests as needed
