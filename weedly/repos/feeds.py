import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from weedly.db.models import Article, Author, Feed
from weedly.errors import AlreadyExistsError, NotFoundError

logger = logging.getLogger(__name__)


class FeedRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str, url: str, is_rss: bool, category: str) -> Feed:
        feed = Feed(name=name, url=url, is_rss=is_rss, category=category)

        try:
            self.session.add(feed)
            self.session.commit()
        except IntegrityError as err:
            raise AlreadyExistsError(entity='feeds', constraint=str(err))

        logger.debug('Feed %s добавлен в БД', url)
        return feed

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

    def ids_by_name(self, name):
        query = self.session.query(Feed)
        query = query.filter_by(is_deleted=False)
        query = query.filter_by(Feed.name.contains(name))
        return query.all()


    def get_all_rss(self, limit: int = 100, offset=0) -> list[Feed]:
        query = self.session.query(Feed)
        query = query.filter_by(is_deleted=False, is_rss=True)
        query = query.limit(limit).offset(offset)
        return query.all()

    def update(self, uid: int, name: str, category: str, url: str, is_rss: bool) -> Feed:
        feed = self.get_by_id(uid)

        feed.name = name
        feed.category = category
        feed.url = url
        feed.is_rss = is_rss

        self.session.commit()

        logger.debug('обновили данные для %S', feed)
        return feed

    def delete(self, uid: int):
        query = self.session.query(Feed)
        query = query.filter_by(uid=uid)
        feed = query.first()
        if not feed:
            raise NotFoundError('feed', uid)

        if feed.is_deleted:
            raise AlreadyExistsError('feed', str(uid))

        feed.is_deleted = True
        self.session.commit()
        logger.debug('удалили Feed %S', feed)
        return True

    def get_authors_by_id(self, uid) -> list[Author]:
        feed = self.get_by_id(uid)
        return feed.feed_authors

    def get_authors_by_name(self, name):
        name = name.replace('-', '.')
        print(name)
        query = self.session.query(Feed)
        query = query.filter_by(is_deleted=False)
        query = query.filter(Feed.name.contains(name)).all()
        if not query:
            raise NotFoundError('feed', name)

        return [e.feed_authors for e in query][0]


    def get_articles(self, uid) -> list[Article]:
        feed = self.get_by_id(uid)
        return feed.feed_articles

if __name__ == '__main__':
    from weedly.db.session import db_session
    repo = FeedRepo(db_session)
    print(repo.get_authors_by_name('vc-ru'))
