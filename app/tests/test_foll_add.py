from fastapi.testclient import TestClient

from ..main import appFastAPI as app

API_KEY = "1"


def test_add_follower_ok():
    with TestClient(app) as client:
        response = client.post(
            url="api/users/1/follow",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 201
    assert response.json()["result"] == True


def test_add_follower_user_not_found():
    with TestClient(app) as client:
        response = client.post(
            url="api/users/1/follow",
            headers={"api-key": "10"},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["result"] == False
    assert response.json()["detail"]["error_message"] == "user not found"


def test_add_follower_has_already_been_set():
    with TestClient(app) as client:
        response = client.post(
            url="/api/users/3/follow",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 400
    assert (
        response.json()["detail"]["error_message"] == "the user is already subscribed"
    )
