from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_login_success():
    response = client.post(
        "/token/login",
        data={"username": "testuser", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_presigned_get_unauth():
    # Should fail without auth
    response = client.post(
        "/presigned/get",
        json={"bucket": "fake", "key": "fake", "expiration": 60},
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.text


def test_bucket_list_unauth():
    response = client.get("/bucket/list?bucket=fake")
    assert response.status_code == 401
    assert "Not authenticated" in response.text
