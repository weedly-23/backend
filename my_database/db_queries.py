'''тут функции для обращения к БД'''

from datetime import datetime
from my_database.models import db, News
import dateutil.parser

def add_news(data:list):
    '''  принимает новости в формате листа словарей вида:
        {
        'title': '',
        'author': '',
        'link': '',
        'source_name':'',
        'publication_date': '',
        'publication_date_parsed': ''
        }
    '''
    for article in data:
        # распарсили дату
        if isinstance(article['published'],list):
            published = datetime(*article['published'][:5])
        elif isinstance(article['published'],str):
            published = dateutil.parser.parse(article['published'])
        else:
            print('неправильный формат даты')

        # проверили, что сочетания ссылка и автор нет в БД. (у одной статьи может быть несколько авторов)
        existing = News.query.filter(News.url == article['url']).filter(News.author == article['author']).count()
        if not existing:
            # добавили в БД
            new = News(title = article['title'], author=article['author'],url=article['url'],
                       source_name=article['source_name'], published = published)
            db.session.add(new)
            db.session.commit()
            print('добавили в БД:', article['title'])
        else:
            print('уже есть---', article['url'])


def fast_add_news(data):
    '''если ключи передаваемых словарей соответствуют полям в таблице News. так быстрее'''
    print(data)
    db.session.bulk_insert_mappings(News, data)
    db.session.commit()


def get_latest_news(how_many = 3):
    '''отдает последние новости в виде списка объектов models.News.
        атрибуты (заголовок, ссылка и тд) можно получить через точку.
    '''
    news = db.session.query(News).order_by(News.published.desc())[:how_many]
    return news

