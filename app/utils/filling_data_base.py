"""module for filling data into a database"""
from datetime import datetime

from sqlalchemy.future import select

from app.database.connect import engine, session
from app.database.models import Follower, Like, Picture, Tweet, User


async def filling_db() -> None:
    """the function of filling the database with data of this"""
    async with engine.begin() as conn:
        res = await session.execute(select(User))
        if not len(res.all()):
            print("*" * 70)
            print("async def add_users()")
            users = [
                User(first_name="Jonn", last_name="Rambo", rating=4, api_key="1"),
                User(first_name="Ar", last_name="Money", api_key="2"),
                User(first_name="Jonn", last_name="Traitorous", rating=5, api_key="3"),
                User(first_name="Kak", last_name="Dam", api_key="4"),
                User(first_name="Lu", last_name="Kang", rating=3, api_key="5"),
                User(
                    first_name="Sheave", last_name="Chevalier", rating=4.5, api_key="6"
                ),
                User(first_name="Princess", last_name="What's-Her-Name", api_key="7"),
            ]
            session.add_all(users)

            tweets = [
                Tweet(
                    user_id=1,
                    content="Сегодня вечерком в покер.",
                    pictures=[1],
                    created_datetime=datetime.now().replace(day=17, microsecond=0),
                ),
                Tweet(
                    user_id=3,
                    content="Сегодня - завтра, будет - вчера. А ещё вчера - сегодня было завтра.",
                    created_datetime=datetime.now().replace(day=18, microsecond=0),
                ),
                Tweet(
                    user_id=5,
                    content="Как такое могло произойти?",
                    created_datetime=datetime.now().replace(day=19, microsecond=0),
                ),
                Tweet(
                    user_id=6,
                    content="Нач -> зам.нач -> зам.зам.нач (Ара зам зам)",
                    pictures=[2, 2, 2],
                    created_datetime=datetime.now().replace(day=20, microsecond=0),
                ),
                Tweet(
                    user_id=6,
                    content="Приютил бездомного котёнка",
                    created_datetime=datetime.now().replace(microsecond=0),
                ),
            ]
            session.add_all(tweets)

            followers = [
                Follower(user_id=1, follower_id=3),
                Follower(user_id=2, follower_id=3),
                Follower(user_id=5, follower_id=2),
                Follower(user_id=6, follower_id=1),
                Follower(user_id=1, follower_id=5),
                Follower(user_id=1, follower_id=6),
            ]
            session.add_all(followers)

            likes = [
                Like(user_id=1, tweet_id=1),
                Like(user_id=2, tweet_id=1),
                Like(user_id=3, tweet_id=1),
                Like(user_id=4, tweet_id=1),
                Like(user_id=1, tweet_id=2),
                Like(user_id=2, tweet_id=2),
                Like(user_id=4, tweet_id=3),
            ]
            session.add_all(likes)

            media = [
                Picture(
                    file_name="/api/medias/Poker-Playing-Cards-tall-l.jpg"
                ),
                Picture(
                    file_name="/api/medias/2731746.png"
                ),
            ]
            session.add_all(media)

            await session.commit()
            print("*" * 70)
