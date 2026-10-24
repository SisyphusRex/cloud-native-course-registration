# Standard Library imports

# Third Party imports
import pytest

# First party imports
from registration_api.app import app
from registration_api.blueprints.courses import COURSE_IDS, COURSES
from registration_api.blueprints.registration import registrations

# Snapshot of the catalog, so tests that update or delete courses don't leak.
ORIGINAL_COURSES = [dict(course) for course in COURSES]


@pytest.fixture
def client():
    registrations.clear()
    # Restore in place; the blueprints hold references to these objects.
    COURSES[:] = [dict(course) for course in ORIGINAL_COURSES]
    COURSE_IDS.clear()
    COURSE_IDS.update(course["id"] for course in COURSES)
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


def test_get_course(client):
    response = client.get("/courses/CS6030")
    assert response.status_code == 200
    assert response.get_json() == {"id": "CS6030", "title": "Cloud Computing"}


def test_get_unknown_course(client):
    response = client.get("/courses/CS9999")
    assert response.status_code == 404


def test_update_course(client):
    response = client.put("/courses/CS6030", json={"title": "Cloud Native Computing"})
    assert response.status_code == 200
    assert response.get_json() == {"id": "CS6030", "title": "Cloud Native Computing"}
    assert {"id": "CS6030", "title": "Cloud Native Computing"} in client.get("/courses").get_json()


@pytest.mark.parametrize("payload", [{}, {"title": ""}, {"title": 123}, None])
def test_update_course_invalid_title(client, payload):
    response = client.put("/courses/CS6030", json=payload)
    assert response.status_code == 400
    assert client.get("/courses/CS6030").get_json()["title"] == "Cloud Computing"


def test_update_unknown_course(client):
    response = client.put("/courses/CS9999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_course(client):
    response = client.delete("/courses/CS6030")
    assert response.status_code == 204
    assert client.get("/courses/CS6030").status_code == 404
    assert len(client.get("/courses").get_json()) == 49

    response = client.post("/register", json={"student": "John Smith", "course": "CS6030"})
    assert response.status_code == 404
    assert registrations == []


def test_delete_unknown_course(client):
    response = client.delete("/courses/CS9999")
    assert response.status_code == 404
