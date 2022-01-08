from datetime import datetime

from pydantic import BaseModel, AnyUrl, ValidationError


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


if __name__ == '__main__':

    urls = ['google.com', 'asd']

    # for e in urls:
    j = """
    {
    "uid":"1",
    "name":"my_name",
    "url": "pydantic-docs.helpmanual.io/usage/types/#urls" }
    """
    f = Feed.parse_raw(j)
    print(f.json())
