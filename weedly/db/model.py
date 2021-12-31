from flask_sqlalchemy import SQLAlchemy
from weedly.db.db import Base, engine
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()


users_n_feeds = Table('users_n_feeds', Base.metadata,
                      Column('user_id', Integer, ForeignKey('user.user_id')),
                      Column('feed_id', Integer, ForeignKey('feeds.feed_id'))
                      )

class Feed(Base):
    ''' атрибуты, доступные через relations:
    Feed.feed_authors
    Feed.feed_articles
    Feed.feed_subs
    '''
    __tablename__ = 'feeds'

    feed_id = Column(Integer, primary_key=True, index=True)
    feed_name = Column(String, index=True)
    category = Column(String)
    rss_link = Column(String, unique=True)

    __tabe_args__ = (UniqueConstraint(feed_name, rss_link), {'extend_existing': True} )

    def __repr__(self):
        return f'Экземпляр Feed: {self.feed_name}'


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=True)
    user_feeds = relationship('Feed', secondary=users_n_feeds, backref='feed_subs')

    def __repr__(self):
        return f'Экземпляр User: {self.user_name}'


class Author(Base):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True)
    author_name = Column(String, nullable=True)
    feed_id = Column(Integer, ForeignKey(Feed.feed_id))
    feed_name = relationship('Feed', foreign_keys=[feed_id], backref='feed_authors')

    __tabe_args__ = (UniqueConstraint(author_name, feed_id), {'extend_existing': True} )

    def __repr__(self):
        return f'Экземпляр Author: {self.author_name}'


class Article(Base):
    __tablename__ = "articles"

    article_id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    published = Column(DateTime)
    feed_id = Column(Integer, ForeignKey(Feed.feed_id))
    feed_name = relationship('Feed', foreign_keys=[feed_id], backref='feed_articles')
    author_id = Column(Integer, ForeignKey(Author.author_id), index=True)
    author_name = relationship('Author', foreign_keys=[author_id], backref='author_articles')

    __tabe_args__ = (UniqueConstraint(url, author_id), {'extend_existing': True} )

    def __repr__(self):
        return f'Экземпляр Article: {self.title}'



if __name__ == "__main__":
    """Run this module if you want to create given tables in a DB."""
    Base.metadata.create_all(bind=engine)
