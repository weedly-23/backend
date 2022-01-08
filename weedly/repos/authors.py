import logging

from sqlalchemy.orm import Session

from weedly.db.models import Author
from weedly.errors import AlreadyExistsError
from weedly.repos.feeds import FeedRepo

logger = logging.getLogger(__name__)


class AuthorRepo:

    def __init__(self, session: Session) -> None:
        self.session = session
        self.feed_repo = FeedRepo(session)

    def add(self, name: str, feed_id, is_deleted=False) -> Author:
        query = self.session.query(Author)
        query = query.filter(Author.name == name, Author.feed_id == feed_id)

        if query.count():
            raise AlreadyExistsError(entity=query.first().name, uid=query.first().uid)

        author_feed = self.feed_repo.get_by_id(feed_id)
        new_author = Author(name=name, feed=author_feed, is_deleted=is_deleted)
        self.session.add(new_author)
        self.session.commit()
        logger.debug('Author %s добавлен в БД', name)
        return new_auth
