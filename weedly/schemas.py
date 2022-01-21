from datetime import datetime

from pydantic import AnyUrl, BaseModel

from typing import Optional


class Model(BaseModel):
    uid: int

    class Config:
        orm_mode = True


class Feed(Model):
    name: str
    category: Optional[str]
    url: AnyUrl
    is_rss: bool


class User(Model):
    name: Optional[str]
    uid: int


class Author(Model):
    name: str
    feed_id: int


class Article(Model):
    title: str
    url: str
    published: datetime
    feed_id: int
    author_id: int
    description: Optional[str]

    class Config:
        arbitrary_types_allowed = True
