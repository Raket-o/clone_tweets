"""the schematics module for answering about the user"""
from typing import List

from pydantic import BaseModel


class Following(BaseModel):
    """Return response data"""

    id: int
    name: str


class Follower(BaseModel):
    """Return response data"""

    id: int
    name: str


class User(BaseModel):
    """Return response data"""

    id: int
    name: str
    followers: List[Follower]
    following: List[Following]


class UserInfo(BaseModel):
    """Return response data"""

    result: bool
    user: User
