from typer import Typer

from weedly.db.db import Base, engine

app = Typer()


@app.command()
def create():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    app()
