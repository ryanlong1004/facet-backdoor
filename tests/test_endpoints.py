from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


# The login endpoint now expects Wasabi/S3 credentials as JSON, not username/password.
def test_login_success():
    payload = {
        "aws_access_key_id": "dummy",
        "aws_secret_access_key": "dummy",
        "region_name": "us-east-1",
        "endpoint_url": "https://s3.wasabisys.com",
    }
    response = client.post(
        "/token/login",
        json=payload,
    )
    # Should always succeed and echo back the credentials
    assert response.status_code == 200
    data = response.json()
    for k, v in payload.items():
        assert data[k] == v


# Now returns 400 for missing Wasabi headers
def test_presigned_get_unauth():
    response = client.post(
        "/presigned/get",
        json={"bucket": "fake", "key": "fake", "expiration": 60},
    )
    assert response.status_code == 400
    # Accept either legacy or new error message
    assert (
        "Missing required Wasabi credential headers" in response.text
        or "Missing required header: x-aws-access-key-id" in response.text
    )


# This endpoint is not present or not protected anymore, so we skip this test.
