import pytest

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root():
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 302)
    assert response.headers["location"].endswith("/static/index.html")

    # Act
    response = client.get("/static/index.html")

    # Assert
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.text

def test_get_activities():
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_and_unregister_activity():
    # Arrange
    email = "testuser@mergington.edu"  # Use a unique email to avoid test pollution
    activity = "Art Club"

    # Act: Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Signup successful
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]

    # Act: Signup again (should fail)
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert: Duplicate signup fails
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

    # Act: Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert: Unregister successful
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

    # Act: Unregister again (should fail)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert: Duplicate unregister fails
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"

def test_signup_activity_not_found():
    # Arrange
    email = "nobody@mergington.edu"
    activity = "NonexistentActivity"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
