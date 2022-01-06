from typing import Optional

from sqlalchemy.orm import Session

from weedly.db.models import User
from weedly.errors import NotFoundError


class UserRepo:

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> None:
        user = User(user_name=name)
        self.session.add(user)
        self.session.commit()

    def get_by_id(self, uid: int) -> Optional[User]:
        query = self.session.query(User)
        query = query.filter_by(user_id=uid)
        query = query.filter_by(is_deleted=False)
        return query.first()

    def get_all(self, limit: int = 100, offset=0) -> list[User]:
        query = self.session.query(User)
        query = query.filter_by(is_deleted=False)
        query = query.limit(limit).offset(offset)
        return query.all()

    def update(self, uid: int, name: str) -> User:
        query = self.session.query(User)
        query = query.filter_by(user_id=uid)
        query = query.filter_by(is_deleted=False)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        user.user_name = name
        self.session.commit()
        return user

    def delete(self, uid: int) -> None:
        query = self.session.query(User)
        query = query.filter_by(user_id=uid)
        user = query.first()
        if not user:
            raise NotFoundError('user', uid)

        user.is_deleted = True
        self.session.commit()
