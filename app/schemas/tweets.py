"""the schematics module for the tweets response"""
from typing import List

from pydantic import BaseModel


class AddTweet(BaseModel):
    """Validate request data"""

    # ...
    tweet_data: str
    tweet_media_ids: List[int] = None


class Author(BaseModel):
    """Return response data"""

    id: int
    name: str


class Like(BaseModel):
    """Return response data"""

    user_id: int
    name: str


class Tweet(BaseModel):
    """Return response data"""

    id: int
    content: str
    attachments: List[str] = None
    author: Author
    likes: List[Like]


class AllTweet(BaseModel):
    """Return response data"""

    # ...
    result: bool
    tweets: List[Tweet]
