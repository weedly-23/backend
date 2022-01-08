from sqlalchemy.orm import Session

from weedly.db.models import Feed, Author, Article
from weedly.errors import NotFoundError, AlreadyExistsError

import logging
logger = logging.getLogger(__name__)


class FeedRepo:

    def __init__(self, session: Session) -> None:
        self.session = session


    def add(self, name: str, url: str, is_rss: bool, is_deleted=False, category="news") -> Feed:
        query = self.session.query(Feed)
        feed = query.filter(Feed.url==url)

        if feed.count():
            logger.error('Feed already exists')
            raise AlreadyExistsError(feed.first().url, feed.first().uid)

        new_feed = Feed(name=name, url=url, is_rss=is_rss, is_deleted=is_deleted, category=category)
        self.session.add(new_feed)
        self.session.commit()
        logger.debug('Feed %s добавлен в БД', url)
        return new_feed

    def get_by_id(self, uid: int) -> Feed:
        query = self.session.query(Feed)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        feed = query.first()
        if not feed:
            raise NotFoundError('feed', uid)

        return feed

    def get_all(self, limit: int = 100, offset=0) -> list[Feed]:
        query = self.session.query(Feed)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        return query.all()

    def update(self, uid: int, name='', category='',
               url='', is_rss='',is_deleted='') -> Feed:
        feed = self.get_by_id(uid)
        args = locals()
        args.pop('uid')
        for k, v in args.items():
            if v:
                setattr(feed, k, v)
                self.session.commit()
        logger.debug('обновили данные для %S', feed)
        return feed

    def delete(self, uid: int) -> None:
        query = self.session.query(Feed)
        query = query.filter_by(uid=uid)
        feed = query.first()
        if not feed:
            raise NotFoundError('feed', uid)

        feed.is_deleted = True
        self.session.commit()
        logger.debug('удалили Feed %S', feed)

    def get_feed_authors(self, uid) -> list[Author]:
        feed = self.get_by_id(uid)
        authors = feed.feed_authors
        if authors:
            return authors

        logger.warning('Feed %s не имеет авторов', feed)
        raise NotFoundError('feed.feed_authors', feed.uid)

    def get_feed_articles(self, uid) -> list[Article]:
        feed = self.get_by_id(uid)
        articles = feed.feed_articles
        if articles:
            return articles

        logger.warning('Feed %s не имеет материалов')
        raise NotFoundError('feed.feed_materials', feed.uid)


if __name__ == '__main__':
    from weedly.db.session import db_session
    f = FeedRepo(db_session)
    f.get_feed_articles(1)
