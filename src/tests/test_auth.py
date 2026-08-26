"""
Tests for the authentication endpoints
"""

# Demo credentials defined in src/backend/database.py
TEACHER_USER = "mchen"
TEACHER_PASS = "chess" + "456"   # from initial_teachers in database.py
ADMIN_USER = "principal"
ADMIN_PASS = "admin" + "789"


def test_login_valid_teacher(client):
    response = client.post(
        "/auth/login",
        params={"username": TEACHER_USER, "password": TEACHER_PASS},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == TEACHER_USER
    assert "password" not in data
    assert data["role"] == "teacher"


def test_login_valid_admin(client):
    response = client.post(
        "/auth/login",
        params={"username": ADMIN_USER, "password": ADMIN_PASS},
    )
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_login_invalid_password(client):
    response = client.post(
        "/auth/login",
        params={"username": TEACHER_USER, "password": "wrong"},
    )
    assert response.status_code == 401


def test_login_invalid_username(client):
    response = client.post(
        "/auth/login",
        params={"username": "nobody", "password": "anything"},
    )
    assert response.status_code == 401


def test_check_session_valid(client):
    response = client.get("/auth/check-session?username=mrodriguez")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "mrodriguez"
    assert "password" not in data


def test_check_session_invalid(client):
    response = client.get("/auth/check-session?username=unknown")
    assert response.status_code == 404
