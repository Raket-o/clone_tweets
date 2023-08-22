from fastapi.testclient import TestClient

from ..main import appFastAPI as app

API_KEY = "1"


def test_get_tweet_ok():
    with TestClient(app) as client:
        response = client.get(
            url="/api/tweets",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 200


def test_get_tweet_user_not_found():
    with TestClient(app) as client:
        response = client.get(
            url="/api/tweets",
            headers={"api-key": "111"},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["result"] == False
    assert response.json()["detail"]["error_message"] == "user not found"


def test_get_info_me_ok():
    with TestClient(app) as client:
        response = client.get(
            url="/api/users/me",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 200


def test_get_info_me_user_not_found():
    with TestClient(app) as client:
        response = client.get(
            url="/api/users/me",
            headers={"api-key": "111"},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["result"] == False
    assert response.json()["detail"]["error_message"] == "user not found"


def test_get_info_any_user_ok():
    with TestClient(app) as client:
        response = client.get(
            url="/api/users/3",
        )

    print(response.json())
    assert response.status_code == 200
