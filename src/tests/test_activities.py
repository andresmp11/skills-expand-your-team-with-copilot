"""
Tests for the activities endpoints
"""


def test_get_activities_returns_all(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_activities_has_expected_fields(client):
    response = client.get("/activities")
    activities = response.json()
    for name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details


def test_get_activities_filter_by_day(client):
    response = client.get("/activities?day=Monday")
    assert response.status_code == 200
    activities = response.json()
    for name, details in activities.items():
        assert "Monday" in details["schedule_details"]["days"]


def test_get_activities_filter_by_start_time(client):
    response = client.get("/activities?start_time=15:00")
    assert response.status_code == 200
    activities = response.json()
    for name, details in activities.items():
        assert details["schedule_details"]["start_time"] >= "15:00"


def test_get_activities_filter_by_end_time(client):
    response = client.get("/activities?end_time=08:00")
    assert response.status_code == 200
    activities = response.json()
    for name, details in activities.items():
        assert details["schedule_details"]["end_time"] <= "08:00"


def test_get_available_days(client):
    response = client.get("/activities/days")
    assert response.status_code == 200
    days = response.json()
    assert isinstance(days, list)
    assert len(days) > 0
    assert "Monday" in days


def test_signup_requires_authentication(client):
    response = client.post("/activities/Chess Club/signup?email=new@mergington.edu")
    assert response.status_code == 401


def test_signup_invalid_teacher(client):
    response = client.post(
        "/activities/Chess Club/signup?email=new@mergington.edu&teacher_username=nobody"
    )
    assert response.status_code == 401


def test_signup_activity_not_found(client):
    response = client.post(
        "/activities/Nonexistent Activity/signup?email=new@mergington.edu&teacher_username=mchen"
    )
    assert response.status_code == 404


def test_signup_already_registered(client):
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu&teacher_username=mchen"
    )
    assert response.status_code == 400


def test_signup_success(client):
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu&teacher_username=mchen"
    )
    assert response.status_code == 200
    assert "newstudent@mergington.edu" in response.json()["message"]

    # Verify the participant was added
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregister_requires_authentication(client):
    response = client.post(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 401


def test_unregister_not_registered(client):
    response = client.post(
        "/activities/Chess Club/unregister?email=notregistered@mergington.edu&teacher_username=mchen"
    )
    assert response.status_code == 400


def test_unregister_success(client):
    # First sign up
    client.post(
        "/activities/Art Club/signup?email=tounregister@mergington.edu&teacher_username=mchen"
    )
    # Then unregister
    response = client.post(
        "/activities/Art Club/unregister?email=tounregister@mergington.edu&teacher_username=mchen"
    )
    assert response.status_code == 200

    activities = client.get("/activities").json()
    assert "tounregister@mergington.edu" not in activities["Art Club"]["participants"]
