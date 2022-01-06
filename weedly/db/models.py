from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import RelationshipProperty, relationship

from weedly.db.db import Base, engine

db = SQLAlchemy()

users_n_feeds = Table(
    'users_n_feeds',
    Base.metadata,
    Column('user_id', ForeignKey('users.user_id')),
    Column('feed_id', ForeignKey('feeds.feed_id')),
)
"""таблица отношений юзеров и фидов"""


class Feed(Base):
    """Класс для источников.

    Бывает двух видов: rss и НЕ-rss.
    Добавляется в БД через DataLoader.add_rss_feed и .add_not_rss_feed соответственно.

    feed_name берется из урла по принципу:
    (https://meduza.io/feature/2022/01/03/neizvestnyy-dvazhdy -> meduza.io)

    Уникальным должно быть сочетание feed_name + source_url.
    В БД могут быть разные source_url с одинаковыми feed_name
    (например, у Коммерсанта есть rss на разные темы)

    Атрибуты, доступные через relations:
    Feed.feed_authors - все авторы фида
    Feed.feed_articles - все статьи фида
    Feed.feed_subs - все юзеры, подписанные на фид
    """

    __tablename__ = 'feeds'

    feed_id = Column(Integer, primary_key=True, index=True)
    feed_name = Column(String, index=True)
    category = Column(String)
    source_url = Column(String, unique=True)
    is_rss_feed = Column(Boolean)

    is_deleted = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint(feed_name, source_url), {'extend_existing': True})

    def __repr__(self) -> str:
        return 'Feed: [{uid}] {name}-{url})'.format(
            uid=self.feed_id,
            name=self.feed_name,
            url=self.source_url,
        )


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=True)
    user_feeds: RelationshipProperty[list['Feed']] = relationship(
        'Feed',
        secondary=users_n_feeds,
        backref='feed_subs',
    )

    is_deleted = Column(Boolean, default=False)

    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f'Экземпляр Users: id -- {self.user_id}'


class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True)
    author_name = Column(String, nullable=True)

    feed_id = Column(Integer, ForeignKey(Feed.feed_id))
    feed_name: RelationshipProperty['Feed'] = relationship(
        'Feed',
        foreign_keys=[feed_id],
        backref='feed_authors',
    )

    is_deleted = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint(author_name, feed_id), {'extend_existing': True})

    def __repr__(self):
        return f'Экземпляр Author: {self.author_name}'


class Article(Base):
    __tablename__ = 'articles'

    article_id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    published = Column(DateTime)

    feed_id = Column(Integer, ForeignKey(Feed.feed_id))
    feed_name: RelationshipProperty['Feed'] = relationship(
        'Feed',
        foreign_keys=[feed_id],
        backref='feed_articles',
    )

    author_id = Column(Integer, ForeignKey(Author.author_id), index=True)
    author_name: RelationshipProperty['Author'] = relationship(
        'Author',
        foreign_keys=[author_id],
        backref='author_articles',
    )

    is_deleted = Column(Boolean, default=False, nullable=True)

    __table_args__ = (UniqueConstraint(url, author_id), {'extend_existing': True})

    def __repr__(self):
        return f'Экземпляр Article: {self.title}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
