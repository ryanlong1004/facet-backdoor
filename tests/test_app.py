from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "openapi" in response.text.lower()


# Add more endpoint tests as needed
