import logging

from typer import Typer

from weedly.db.session import create_db, db_session
from weedly.db.models import Feed
from weedly.db.test_rss import test_rss_sources

app = Typer()
logger = logging.getLogger(__name__)


@app.command()
def create():
    create_db()
    logger.debug('Создали базку!')


@app.command()
def add_test_rss():
    for source in test_rss_sources:
        db_session.add(Feed(**source))
        db_session.commit()

    logger.debug('добавили в БД тестовые rss!')


if __name__ == '__main__':
    app()
