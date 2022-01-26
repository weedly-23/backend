from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from weedly.db.models import Channel
from weedly.errors import NotFoundError, AlreadyExistsError

class ChannelRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, title: str, channel_id: str) -> Channel:
        try:
            channel = Channel(title=title, channel_id=channel_id)
            self.session.add(channel)
            self.session.commit()
            return channel
        except IntegrityError as err:
            raise AlreadyExistsError(entity='channels', constraint=str(err))

    def get_by_uid(self, uid: int) -> Channel:
        query = self.session.query(Channel)
        query = query.filter_by(uid=uid)
        channel = query.first()
        if not channel:
            raise NotFoundError('channel', uid)
        return channel

    def delete(self, uid: int) -> None:
        ...

    def get_all(self, limit: int=100) -> list[Channel]:
        ...

