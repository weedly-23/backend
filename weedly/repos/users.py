from typing import Optional

from sqlalchemy.orm import Session

from weedly.db.models import User, Feed
from weedly.errors import NotFoundError


class UserRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, uid: int, feed_id: Optional[int], name: Optional[str]) -> User:
        deleted_user = self.session.query(User).filter_by(uid=uid, is_deleted=True).first()
        if deleted_user:
            deleted_user.is_deleted = False
            self.session.commit()
            return deleted_user

        user = User(uid=uid, name=name)
        self.session.add(user)
        self.session.commit()
        return user

    def get_by_id(self, uid: int) -> User:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        return user

    def get_all(self, limit: int = 100, offset=0) -> list[User]:
        query = self.session.query(User)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        return query.all()

    def update(self, uid: int, name: Optional[str], feed_id: Optional[int]) -> User:
        """изменение имени, подписка на rss"""
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()

        if not user:
            raise NotFoundError('user', uid)

        if name:
            user.name = name

        if feed_id:
            feed = self.session.query(Feed).filter_by(uid=feed_id, is_deleted=False).first()
            user.feeds.append(feed)

        self.session.commit()
        return user

    def delete_rss_from_subs(self, uid, feed_id):
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        updated_feeds = [feed for feed in user.feeds if feed.uid != feed_id]
        user.feeds = updated_feeds
        self.session.commit()

        return user.feeds

    def delete(self, uid: int) -> None:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        user.is_deleted = True
        self.session.commit()
