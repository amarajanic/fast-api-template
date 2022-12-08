from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_blog_create():
    response =  client.post(
        "/blogs", 
        json={"title": "test_title", "body": "test_body", "user_id": 1}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["title"] == "test_title"
    user_id = data["user"]["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == user_id