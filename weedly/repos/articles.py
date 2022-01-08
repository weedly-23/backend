from datetime import datetime

from sqlalchemy.orm import Session

from weedly.db.models import Article
from weedly.errors import NotFoundError


class ArticleRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str, url: str, published: datetime) -> Article:
        article = Article(name=name, url=url, published=published)
        self.session.add(article)
        self.session.commit()
        return article

    def get_by_id(self, uid: int) -> Article:
        query = self.session.query(Article)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        article = query.first()
        if not article:
            raise NotFoundError('article', uid)

        return article

    def get_all(self, limit: int = 100, offset=0) -> list[Article]:
        query = self.session.query(Article)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        return query.all()

    def update(self, uid: int, name: str, url: str, published: datetime) -> Article:
        query = self.session.query(Article)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        article = query.first()
        if not article:
            raise NotFoundError('article', uid)
        article.name = name
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
