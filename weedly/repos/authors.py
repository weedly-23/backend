import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from weedly.db.models import Author
from weedly.errors import AlreadyExistsError

logger = logging.getLogger(__name__)


class AuthorRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str, feed_id, is_deleted=False) -> Author:
        new_author = Author(name=name, feed_id=feed_id, is_deleted=is_deleted)

        try:
            self.session.add(new_author)
            self.session.commit()
        except IntegrityError as err:
            raise AlreadyExistsError(entity='authors', constraint=str(err))

        logger.debug('Author %s добавлен в БД', name)

        return new_author
