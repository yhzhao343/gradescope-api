import pytest
from fastapi.testclient import TestClient
from sylveon.api.api import (
    api,
    get_assignment_submission,
    get_assignments,
    get_course_memberships,
    get_courses,
    get_extensions,
    update_assignment_due_date,
    update_assignment_late_due_date,
    update_assignment_release_date,
    update_student_due_date,
    update_student_late_due_date,
    update_student_release_date,
    login,
    root,
)

client = TestClient(api)

# Mock token data for testing
token = {"token": "sample_token"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_login():
    response = client.post(
        "/login", json={"username": "mock_user", "password": "mock_pswd"}
    )
    assert response.status_code == 200
    assert response.json() == {"token": "sample_token"}


def test_get_courses():
    response = client.get("/account", headers={"Authorization": "Bearer token"})
    assert response.status_code == 200
    assert response.json() == {"courses": []}


def test_update_assignment_due_date():
    response = client.put(
        "/assignment/due_date",
        headers={"Authorization": "Bearer token"},
        json={"assignment_id": "assignment_id", "due_date": "due_date"},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Assignment due date updated"}
