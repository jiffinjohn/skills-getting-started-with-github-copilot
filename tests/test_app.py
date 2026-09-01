from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "student@mergington.edu"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    activities[activity_name]["participants"] = [email, "daniel@mergington.edu"]

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
