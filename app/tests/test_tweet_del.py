import asyncio
from datetime import datetime

from fastapi.testclient import TestClient

from ..database.transactions import add_tweet_db
from ..main import appFastAPI as app

API_KEY = "1"


def test_del_tweet_ok():
    with TestClient(app) as client:
        response = client.delete(
            url="/api/tweets/1",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 200
    assert response.json()["result"] == True


def test_del_tweet_user_not_found():
    with TestClient(app) as client:
        response = client.delete(
            url="/api/tweets/1",
            headers={"api-key": "10"},
        )
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["result"] == False
    assert response.json()["detail"]["error_message"] == "user not found"


def test_del_tweet_not_found():
    with TestClient(app) as client:
        response = client.delete(
            url="/api/tweets/111",
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["error_message"] == "tweet not found"
