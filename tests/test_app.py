from fastapi.testclient import TestClient

import src.app as app_module


def test_root_redirect(client: TestClient):
    # Arrange / Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_activity_keys(client: TestClient):
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload
    assert payload["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_adds_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {student_email} for {activity_name}"}
    assert student_email in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_again_returns_400(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_to_missing_activity_returns_404(client: TestClient):
    # Arrange
    activity_name = "Unknown Club"
    student_email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_removes_participant(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {student_email} from {activity_name}"}
    assert student_email not in app_module.activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_400(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    student_email = "newstudent@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_from_missing_activity_returns_404(client: TestClient):
    # Arrange
    activity_name = "Unknown Club"
    student_email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
