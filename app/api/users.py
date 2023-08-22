"""user route processing module"""
from typing import Any, Dict

from fastapi import APIRouter, Request

from app.database.transactions import (
    del_follow_user_db,
    follow_user_db,
    get_user_info_db,
)
from app.schemas import users

router = APIRouter(prefix='/users')


@router.post(
    path="/{id}/follow",
    response_description="",
    response_model="",
    status_code=201,
)
async def follow_tweet(request: Request, id: int) -> Dict[str, bool] | None:
    """the function handles the router adding subscriptions"""
    api_key = request.headers.get("api-key")
    res = await follow_user_db(api_key=api_key, user_id_follow=id)
    return res


@router.delete(
    path="/{id}/follow",
    response_description="",
    response_model="",
    status_code=200,
)
async def del_follow_tweet(request: Request, id: int) -> Dict[str, bool] | None:
    """the function processes the router by deleting a follow"""
    api_key = request.headers.get("api-key")
    res = await del_follow_user_db(api_key=api_key, user_id_follow=id)
    return res


@router.get(
    path="/me",
    response_model=users.UserInfo,
    response_model_exclude_unset=True,
    status_code=200,
)
async def get_about_me(
    request: Request,
) -> Dict[str, bool | Dict[str, str | Any]] | None:
    """the function processes the router to output information about itself"""
    api_key = request.headers.get("api-key")
    res = await get_user_info_db(api_key=api_key)
    return res


@router.get(
    path="/{id}",
    response_model=users.UserInfo,
    response_model_exclude_unset=True,
    status_code=200,
)
async def get_user_info(id: int) -> Dict[str, bool | Dict[str, str | Any]] | None:
    """the function processes the router for the output of user information"""
    res = await get_user_info_db(user_id=id)
    return res
