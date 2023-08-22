"""module for working with transactions"""
from datetime import datetime
from typing import Any, Dict, List

import asyncpg
from sqlalchemy import text
from sqlalchemy.future import select

from app.schemas import tweets
from app.utils.send_error import send_error
from config_data.config import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER

from .connect import engine, session
from .tables import Follower, Like, Picture, Tweet, User


async def create_db() -> None:
    cursor = await asyncpg.connect(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"
    )
    await cursor.execute("CREATE DATABASE news_posts;")


async def get_user_id(api_key: str) -> int:
    """the function finds the user by api_key and returns his id, otherwise it will return 0."""
    user = await session.execute(select(User).where(User.api_key == api_key))
    user = user.scalar()

    if user:
        return user.id

    return 0


async def add_tweet_db(
    api_key: str, data: tweets.AddTweet
) -> dict[str, bool | int] | None:
    """the function adds a new tweet to the database"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        user_id = await send_error(error_message="user not found")
        return user_id
    try:
        media_ids = data.tweet_media_ids

        new_tweet = Tweet(
            user_id=user_id,
            content=data.tweet_data,
            pictures=media_ids,
            created_datetime=datetime.now(),
        )

        session.add(new_tweet)

        if media_ids != [] and media_ids[0] != 0:
            for i_media in media_ids:
                media = await session.execute(
                    select(Picture).where(Picture.id == i_media)
                )
                media = media.scalar()
                media.tweet_id = new_tweet.id

        await session.commit()
        res = {"result": True, "tweets_id": new_tweet.id}
        return res

    except AttributeError:
        await session.rollback()
        res = await send_error(error_message="media not found")
        return res


async def add_medias_db(api_key: str, file_name: str) -> Dict[str, bool | int] | None:
    """the function adds a new medias to the database"""
    user_id = await get_user_id(api_key=api_key)

    if not user_id:
        user_id = await send_error(error_message="user not found")
        return user_id

    file_name = f"/api/medias/{file_name}"

    pic = Picture(file_name=file_name)

    print("pic"*15, pic)

    req = f"INSERT INTO pictures (file_name) VALUES ('{file_name}') RETURNING id;"
    pic_id = await session.execute(text(req))
    pic_id = pic_id.one_or_none()

    res = {"result": True, "media_id": pic_id[0]}
    return res


async def del_tweet_db(api_key: str, tweet_id: int) -> Dict[str, bool] | None:
    """the function removes the tweet from the database"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        res = await send_error(error_message="user not found")
        return res

    tweet = await session.execute(
        select(Tweet).where(Tweet.user_id == user_id, Tweet.id == tweet_id)
    )
    tweet = tweet.one_or_none()
    if not tweet:
        res = await send_error(error_message="tweet not found")
        return res

    if tweet:
        await session.delete(tweet[0])
        await session.commit()
        res = {"result": True}
        return res


async def like_tweet_db(api_key: str, tweet_id: int) -> Dict[str, bool] | None:
    """the function adds a like to the database"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        res = await send_error(error_message="user not found")
        return res

    check_tweet = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
    check_tweet = check_tweet.one_or_none()
    if not check_tweet:
        res = await send_error(error_message="tweet not found")
        return res

    like = await session.execute(
        select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
    )
    like = like.one_or_none()

    if like:
        res = await send_error(error_message="the user has already put a like")
        return res

    if user_id and not like:
        like_new = Like(user_id=user_id, tweet_id=tweet_id)
        session.add(like_new)
        await session.commit()
        res = {"result": True}
        return res


async def del_like_tweet_db(api_key: str, tweet_id: int) -> Dict[str, bool] | None:
    """the function removes the like from the database"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        res = await send_error(error_message="user not found")
        return res

    check_tweet = await session.execute(select(Tweet).where(Tweet.id == tweet_id))
    check_tweet = check_tweet.one_or_none()
    if not check_tweet:
        res = await send_error(error_message="tweet not found")
        return res

    like = await session.execute(
        select(Like).where(Like.user_id == user_id, Like.tweet_id == tweet_id)
    )
    like = like.one_or_none()

    if not like:
        res = await send_error(error_message="user no put a like")
        return res

    await session.delete(like[0])
    await session.commit()
    res = {"result": True}
    return res


async def follow_user_db(api_key: str, user_id_follow: int) -> Dict[str, bool] | None:
    """the function adds a follow to the database"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        res = await send_error(error_message="user not found")
        return res

    follow = await session.execute(
        select(Follower).where(
            Follower.user_id == user_id, Follower.follower_id == user_id_follow
        )
    )
    follow = follow.one_or_none()

    check_follower_id = await session.execute(
        select(User).where(User.id == user_id_follow)
    )
    check_follower_id = check_follower_id.one_or_none()
    if not check_follower_id:
        res = await send_error(error_message="follower not found")
        return res

    if follow:
        res = await send_error(error_message="the user is already subscribed")
        return res

    follow = Follower(user_id=user_id, follower_id=check_follower_id[0].id)
    session.add(follow)
    await session.commit()
    res = {"result": True}
    return res


async def del_follow_user_db(
    api_key: str, user_id_follow: int
) -> Dict[str, bool] | None:
    """the function removes the follow from the database"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        res = await send_error(error_message="user not found")
        return res

    follow = await session.execute(
        select(Follower).where(
            Follower.user_id == user_id, Follower.follower_id == user_id_follow
        )
    )
    follow = follow.one_or_none()

    check_follower_id = await session.execute(
        select(User).where(User.id == user_id_follow)
    )
    check_follower_id = check_follower_id.one_or_none()
    if not check_follower_id:
        res = await send_error(error_message="follower not found")
        return res

    if not follow:
        res = await send_error(error_message="user no put a follow")
        return res

    await session.delete(follow[0])
    await session.commit()
    res = {"result": True}
    return res


async def get_tweets_db(
    api_key: str,
) -> Dict[
    str,
    str
    | List[
        Dict[str, list[Any] | Dict[str, str | Any] | List[dict[str, str | Any]] | Any]
    ],
] | None:
    """the function issues a tweet from subscribed users.
    Tweets are sorted by user rating and creation date"""
    user_id = await get_user_id(api_key=api_key)
    if not user_id:
        res = await send_error(error_message="user not found")
        return res

    req = f"""
        SELECT follower_id, first_name, last_name
        FROM followers as fol
        JOIN public.users u on u.id = fol.follower_id
        WHERE user_id = {user_id}
        ORDER BY u.rating DESC;
    """

    subscriptions = await session.execute(text(req))
    subscriptions = subscriptions.all()

    tweets = []
    for i_subscr in subscriptions:
        tweets_info = await session.execute(
            select(Tweet)
            .where(Tweet.user_id == i_subscr[0])
            .order_by(Tweet.created_datetime.desc())
        )
        tweets_info = tweets_info.all()

        for i_tweet in tweets_info:
            tweet = dict()
            tweet["id"] = i_tweet[0].id
            tweet["content"] = i_tweet[0].content
            medias = i_tweet[0].pictures
            if medias is not None and medias != 0:
                attachments = []
                for i_media in medias:
                    media = await session.execute(
                        select(Picture).where(Picture.id == i_media)
                    )
                    media = media.scalar()
                    attachments.append(media.file_name)

                tweet["attachments"] = attachments
                tweet["attachments"] = attachments

            else:
                attachments = []

            tweet["attachments"] = attachments
            tweet["author"] = {
                "id": i_subscr[0],
                "name": f"{i_subscr[1]} {i_subscr[2]}",
            }

            likes = await session.execute(
                select(Like, User).join(User).where(Like.tweet_id == i_tweet[0].id)
            )
            likes = likes.all()

            likes_list = [
                {
                    "user_id": i_like[1].id,
                    "name": f"{i_like[1].first_name} {i_like[1].last_name}",
                }
                for i_like in likes
            ]

            tweet["likes"] = likes_list

            tweets.append(tweet)

    dict_answer = {"result": True, "tweets": tweets}
    return dict_answer


async def get_user_info_db(
    api_key: str = None, user_id: int = 0
) -> Dict[str, bool | Dict[str, str | Any]] | None:
    """the function provides information about the user"""
    if api_key == "test":
        api_key = "0"
        guest = User(api_key="0", first_name="Guest", last_name="", rating=0)
        session.add(guest)
        await session.commit()

    if api_key:
        user_id = await get_user_id(api_key=api_key)
        if not user_id:
            res = await send_error(error_message="user not found")
            return res

        user_info = await session.execute(select(User).where(User.api_key == api_key))
        user_info = user_info.scalar()
    else:
        user_info = await session.execute(select(User).where(User.id == user_id))
        user_info = user_info.scalar()

    if not user_info:
        res = await send_error(error_message="user not found")
        return res

    req = f"""
        SELECT followers.id, u.first_name, u.last_name
        FROM followers
        JOIN users u on u.id = followers.follower_id
        WHERE user_id = {user_id};
    """
    followers = await session.execute(text(req))
    followers = followers.all()
    followers_list = [
        {"id": i.id, "name": f"{i.first_name} {i.last_name}"} for i in followers
    ]

    req = f"""
        SELECT u.id, u.first_name, u.last_name
        FROM followers
        JOIN users u on u.id = followers.user_id
        WHERE follower_id = {user_id};
    """
    following = await session.execute(text(req))
    following = following.all()
    following_list = [
        {"id": i.id, "name": f"{i.first_name} {i.last_name}"} for i in following
    ]

    dict_answer = dict()
    dict_answer["result"] = True
    dict_answer["user"] = {
        "id": user_info.id,
        "name": f"{user_info.first_name} {user_info.last_name}",
    }
    dict_answer["user"]["followers"] = followers_list
    dict_answer["user"]["following"] = following_list

    return dict_answer
