import logging

from typer import Typer

from weedly.db.session import create_db

app = Typer()
logger = logging.getLogger(__name__)


@app.command()
def create():
    create_db()
    logger.warning('Создали базку!')

#Article(title='Tesla отложила производство электрического пикапа Cybertruck до\xa02023 года', link='https://meduza.io/news/2022/01/14/tesla-otlozhila-proizvodstvo-elektricheskogo-pikapa-cybertruck-do-2023-goda', author=None, published=<Arrow [2022-01-14T08:00:33+00:00]>, description=None)

if __name__ == '__main__':
    from weedly.db.models import Article
    from weedly.db.session import engine
    Article.__table__.drop(engine)

    app()
