"""tweet routs processing module"""
from typing import Any

from fastapi import APIRouter, Request

from app.database.transactions import (
    add_tweet_db,
    del_follow_user_db,
    del_like_tweet_db,
    del_tweet_db,
    get_tweets_db,
    like_tweet_db,
)
from app.schemas import tweets

router = APIRouter(prefix='/tweets')


@router.post(path="/", status_code=201)
async def add_tweet(
    request: Request, data: tweets.AddTweet
) -> dict[str, bool | int] | dict[str, bool | str]:
    """the function processes the router by adding a new tweet"""
    api_key = request.headers.get("api-key")
    res = await add_tweet_db(api_key=api_key, data=data)
    return res


@router.delete(
    path="/{id}/follow",
    response_description="",
    response_model="",
    status_code=200,
)
async def del_follow_tweet(request: Request, id: int) -> dict[str, bool] | None:
    """the function processes the router by deleting subscribers"""
    api_key = request.headers.get("api-key")
    res = await del_follow_user_db(api_key=api_key, user_id_follow=id)
    return res


@router.delete(
    path="/{id}", response_description="", response_model="", status_code=200
)
async def del_tweet(request: Request, id: int) -> dict[str, bool] | None:
    """the function handles the route by deleting the tweet"""
    api_key = request.headers.get("api-key")
    res = await del_tweet_db(api_key=api_key, tweet_id=id)
    return res


@router.post(
    path="/{id}/likes",
    response_description="",
    response_model="",
    status_code=201,
)
async def like_tweet(request: Request, id: int) -> dict[str, bool] | None:
    """the function processes the router by adding a like tweet"""
    api_key = request.headers.get("api-key")
    res = await like_tweet_db(api_key=api_key, tweet_id=id)
    return res


@router.delete(
    path="/{id}/likes",
    response_description="",
    response_model="",
    status_code=200,
)
async def del_like_tweet(request: Request, id: int) -> dict[str, bool] | None:
    """the function processes the router by deleting a like tweet"""
    api_key = request.headers.get("api-key")
    res = await del_like_tweet_db(api_key=api_key, tweet_id=id)
    return res


@router.get(
    path="/",
    response_model=tweets.AllTweet,
    response_model_exclude_unset=True,
    status_code=200,
)
async def get_tweets(
    request: Request,
) -> dict[
    str,
    str
    | list[
        dict[str, list[Any] | dict[str, str | Any] | list[dict[str, str | Any]] | Any]
    ],
] | None | dict[str, str]:
    """the function processes the router by tweets output"""
    api_key = request.headers.get("api-key")

    res = await get_tweets_db(api_key=api_key)
    return res
