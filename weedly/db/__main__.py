import logging

from typer import Typer

from weedly.db.session import Base, engine

app = Typer()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


@app.command()
def create():
    Base.metadata.create_all(bind=engine)
    logger.warning('Создали базку!')


if __name__ == '__main__':
    app()
