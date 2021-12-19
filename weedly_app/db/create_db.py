'''создаем базу локально и заполняем ее тестоыми данными'''
import typer
from weedly_app import create_app
from weedly_app.tools.news_loader import get_test_news_for_db, get_news_from_file
from weedly_app.db.db_queries import add_news
from weedly_app.db.models import db, News


typer_app = typer.Typer()

@typer_app.command()
def create_news_db(fill_with_data:bool = False):
    app = create_app()
    with app.app_context():
        db.create_all(app=app)
        if fill_with_data:
            test_news = get_test_news_for_db()
            add_news(test_news)


@typer_app.command()
def add_news_from_file(file):
    app = create_app()
    with app.app_context():
        db.create_all(app=app)
        articles = get_news_from_file(file)
        add_news(articles)


@typer_app.command()
def reset_news_table():
    app = create_app()
    with app.app_context():
        all_news = db.session.query(News).filter().delete()
        db.session.commit()
        print('удалили все новости из БД')


if __name__ == '__main__':
    typer_app()
