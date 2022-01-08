from datetime import datetime

from pydantic import AnyUrl, BaseModel


class Model(BaseModel):
    uid: int

    class Config:
        orm_mode = True


class Feed(Model):
    name: str
    category: str
    url: AnyUrl
    is_rss: bool


class User(Model):
    name: str


class Author(Model):
    name: str
    feed_id: int


class Article(Model):
    name: str
    url: str
    published: datetime
