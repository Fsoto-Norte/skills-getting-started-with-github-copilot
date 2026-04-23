import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Asegurarse de que el usuario no esté inscrito
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

def test_signup_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    # Inscribir una vez
    client.delete(f"/activities/{activity}/participants/{email}")
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Intentar inscribir de nuevo
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]

def test_remove_participant():
    email = "testremove@mergington.edu"
    activity = "Drama Club"
    # Inscribir primero
    client.post(f"/activities/{activity}/signup", params={"email": email})
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code in (200, 307, 302)
