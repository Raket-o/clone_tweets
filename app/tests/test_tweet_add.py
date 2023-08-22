import asyncio
from datetime import datetime

from fastapi.testclient import TestClient

from ..database.transactions import add_tweet_db
from ..main import appFastAPI as app

API_KEY = "1"
TWEET = {"tweet_data": "Test tweet.", "tweet_media_ids": [1]}


def test_add_tweet_ok():
    with TestClient(app) as client:
        response = client.post(
            url="/api/tweets",
            json=TWEET,
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 201
    assert response.json()["result"] == True
    assert response.json()["tweets_id"] == 6


def test_add_tweet_user_not_found():
    with TestClient(app) as client:
        response = client.post(
            url="/api/tweets",
            json=TWEET,
            headers={"api-key": "10"},
        )

    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"]["result"] == False
    assert response.json()["detail"]["error_message"] == "user not found"


def test_add_tweet_field_required():
    tweet = {"tweet_media_ids": [1]}

    with TestClient(app) as client:
        response = client.post(
            url="/api/tweets",
            json=tweet,
            headers={"api-key": API_KEY},
        )

    print(response.json())
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"
