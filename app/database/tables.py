"""the module for creating tables"""
import datetime
from typing import Any, Dict

from sqlalchemy import ARRAY, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .connect import Base


class User(Base):
    """class for creating a table"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String(200), nullable=False)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)
    rating = Column(Float, default=0)

    follower = relationship(
        "Follower",
        cascade="all, delete",
        backref="users",
        passive_deletes=True,
        lazy=True,
    )
    like = relationship(
        "Like", cascade="all, delete", backref="users", passive_deletes=True, lazy=True
    )
    tweet = relationship(
        "Tweet", cascade="all, delete", backref="users", passive_deletes=True, lazy=True
    )

    def __repr__(self) -> str:
        """a function that returns a printed representation of a given object"""
        return f'"id" {self.id}, "first_name": {self.first_name}, "last_name": {self.last_name}'


class Tweet(Base):
    """class for creating a table"""

    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(String(200), nullable=False)
    pictures = Column(ARRAY(Integer))
    created_datetime = Column(DateTime, default=datetime.datetime.now())

    like = relationship(
        "Like", cascade="all, delete", backref="tweets", passive_deletes=True, lazy=True
    )

    def __repr__(self) -> str:
        """a function that returns a printed representation of a given object"""
        return (
            f'"id": {self.id}, "content": {self.content}, "pictures": {self.pictures}'
        )


class Follower(Base):
    """class for creating a table"""

    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    follower_id = Column(Integer)

    def __repr__(self) -> str:
        """a function that returns a printed representation of a given object"""
        return f'"id" {self.id}, "user_id": {self.user_id}, "follower_id": {self.follower_id}'


class Like(Base):
    """class for creating a table"""

    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        """a function that returns a printed representation of a given object"""
        return f'"id" {self.id}, "user_id": {self.user_id}, "tweet_id": {self.tweet_id}'


class Picture(Base):
    """class for creating a table"""

    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(200), nullable=True)

    def __repr__(self) -> str:
        """a function that returns a printed representation of a given object"""
        return f'"id": {self.id}, "attachments": {self.file_name}'
