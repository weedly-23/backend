import logging
logger = logging.getLogger(__name__)
from sqlalchemy.orm import Session

from weedly.db.models import Author
from weedly.repos.feeds import FeedRepo
from weedly.errors import AlreadyExistsError
import logging
logger = logging.getLogger(__name__)


class AuthorRepo:

    def __init__(self, session: Session) -> None:
        self.session = session
        self.feed_repo = FeedRepo(session)

    def add(self, name: str, feed_id, is_deleted=False) -> Author:
        existing_author = self.session.query(Author).filter(Author.name==name,
                                                            Author.feed_id==feed_id)
        if existing_author.count():
            logger.error('Author already exists')
            raise AlreadyExistsError(entity=existing_author.first().name,
                                     uid=existing_author.first().uid)

        author_feed = self.feed_repo.get_by_id(feed_id)
        new_author = Author(name=name, feed=author_feed, is_deleted=is_deleted)
        self.session.add(new_author)
        self.session.commit()
        logger.debug('Author %s добавлен в БД', name)
        return new_author


if __name__ == '__main__':
    from weedly.db.session import db_session
    a = AuthorRepo(db_session)
    a.add('Имя автора', 1)


