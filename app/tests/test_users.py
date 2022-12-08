from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_user_found():
    response = client.get(f"/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "amar@gmail.com"
    assert data["name"] == "amar"
