from typing import Optional

from sqlalchemy.orm import Session

from weedly.db.models import Article, Feed, User
from weedly.errors import NotFoundError


class UserRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, uid: int, name: Optional[str]) -> User:
        query = self.session.query(User)
        user = query.filter_by(uid=uid).first()
        if user and user.is_deleted:
            user.is_deleted = False
            self.session.commit()

        if not user:
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

    def add_rss_to_user(self, uid: int, feed_id: int) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()

        if not user:
            raise NotFoundError('user', uid)

        query = self.session.query(Feed)
        feed = query.filter_by(uid=feed_id, is_deleted=False).first()
        if not feed:
            raise NotFoundError('feeds', feed_id)

        user.feeds.append(feed)

        self.session.commit()
        return user.feeds

    def delete_rss_from_subs(self, uid: int, feed_id: int) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        updated_feeds = [feed for feed in user.feeds if feed.uid != feed_id]
        if user.feeds == updated_feeds:
            raise NotFoundError('юзер не подписан на этот фид', uid)

        user.feeds = updated_feeds
        self.session.commit()
        return user.feeds

    def get_user_rss(self, uid) -> list[Feed]:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        return user.feeds

    def get_not_notificated_articles(self, user_id) -> list[Article]:
        query = self.session.query(User)
        query = query.filter_by(uid=user_id)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', user_id)

        all_not_notificated_articles = []

        for feed in user.feeds:
            for article in feed.feed_articles:
                notificated_users = [user.uid for user in article.notificated_users]
                if user_id not in notificated_users:
                    all_not_notificated_articles.append(article)
                    article.notificated_users.append(user)
                    self.session.commit()

        return all_not_notificated_articles

    def delete(self, uid: int) -> None:
        query = self.session.query(User)
        query = query.filter_by(uid=uid)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        user.is_deleted = True
        self.session.commit()
