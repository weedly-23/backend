from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from weedly.db.models import Article, Feed

from weedly.errors import NotFoundError, AlreadyExistsError


class ArticleRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(
        self, title: str, url: str,
        published: datetime,
        author_id: int, feed_id: int
    ) -> Article:

        try:
            article = Article(title=title, url=url, published=published,
                              feed_id=feed_id, author_id=author_id)
            print(article)
            self.session.add(article)
            self.session.commit()
            return article
        except IntegrityError as err:
            raise AlreadyExistsError(entity='authors', constraint=str(err))

    def get_by_id(self, uid: int) -> Article:
        query = self.session.query(Article)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        article = query.first()
        if not article:
            raise NotFoundError('article', uid)

        return article

    def get_by_feed_name(self, feed_name) -> list[Article]:
        query = self.session.query(Feed)
        query = query.filter(Feed.name.contains(feed_name))
        if not query.count():
            raise NotFoundError('feed_name', feed_name)

        articles = [feed.feed_articles for feed in query]

        if not articles:
            raise NotFoundError('articles', feed_name)

        return articles

    def get_all(self, limit: int = 100, offset=0) -> list[dict[str, str]]:
        query = self.session.query(Article)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        query = query.all()
        return query

    def update(self, uid: int, title: str, url: str, published: datetime) -> Article:
        query = self.session.query(Article)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        article = query.first()
        if not article:
            raise NotFoundError('article', uid)
        article.title = title
        article.url = url
        article.published = published
        self.session.commit()
        return article

    def delete(self, uid: int) -> None:
        query = self.session.query(Article)
        query = query.filter_by(uid=uid)
        article = query.first()
        if not article:
            raise NotFoundError('article', uid)

        article.is_deleted = True
        self.session.commit()
