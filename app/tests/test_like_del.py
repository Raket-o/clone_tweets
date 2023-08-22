from fastapi.testclient import TestClient

from ..main import appFastAPI as app

API_KEY = "1"


def test_add_like_ok():
    with TestClient(app) as client:
        response = client.delete(
            url="/api/tweets/2/likes",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["result"] == True


def test_add_tweet_user_not_found():
    with TestClient(app) as client:
        response = client.delete(
            url="/api/tweets/2/likes",
            headers={"api-key": "10"},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["result"] == False
    assert response.json()["detail"]["error_message"] == "user not found"


def test_add_like_has_already_been_set():
    with TestClient(app) as client:
        response = client.delete(
            url="/api/tweets/3/likes",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["error_message"] == "user no put a like"
