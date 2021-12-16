'''создаем базу локально и заполняем ее тестоыми данными'''
from my_database.db_queries import add_news
from weedly_app.tools.news_loader import get_test_news_for_db
from my_database.models import db


def create_db():
    from weedly_app import create_app
    db.create_all(app=create_app())


def fill_db_with_test_data():
    from weedly_app import create_app
    app = create_app()
    with app.app_context():
        test_news = get_test_news_for_db()
        add_news(test_news)


if __name__ == '__main__':
    create_db()
    fill_db_with_test_data()
