import logging

from typer import Typer

from weedly.db.session import create_db

app = Typer()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


@app.command()
def create():
    create_db()
    logger.warning('Создали базку!')


if __name__ == '__main__':
    app()
