from typing import Any


class AppError(Exception):
    """Application errors."""


class NotFoundError(AppError):

    def __init__(self, entity: str, uid: Any) -> None:
        super().__init__(f'Not found {entity} [{uid}]')
        self.entity = entity
        self.uid = uid
