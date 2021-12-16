from my_database.models import db
from weedly_app import create_app

from my_database.db_queries import add_news
from weedly_app.tools.news_loader import get_test_news_for_db

db.create_all(app=create_app())

# берем новости, которые лежат локально и загружаем их в нашу БД для теста
test_news = get_test_news_for_db()
add_news(test_news)




