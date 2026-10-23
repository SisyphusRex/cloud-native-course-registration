# Standard Library imports

# Third Party imports
import pytest

# First party imports
from registration_api.app import app, registrations


@pytest.fixture
def client():
    registrations.clear()
    return app.test_client()


def test_list_courses(client):
    response = client.get("/courses")
    assert response.status_code == 200
    courses = response.get_json()
    assert len(courses) == 50
    assert {"id": "CS6030", "title": "Cloud Computing"} in courses


def test_register(client):
    response = client.post("/register", json={"student": "John Smith", "course": "CS6030"})
    assert response.status_code == 201
    assert response.get_json() == {"status": "registered"}
    assert registrations == [{"student": "John Smith", "course": "CS6030"}]


@pytest.mark.parametrize(
    "payload",
    [
        {"course": "CS6030"},
        {"student": "", "course": "CS6030"},
        {"student": "John Smith"},
        None,
    ],
)
def test_register_missing_fields(client, payload):
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert registrations == []


def test_register_unknown_course(client):
    response = client.post("/register", json={"student": "John Smith", "course": "CS9999"})
    assert response.status_code == 404
    assert registrations == []
