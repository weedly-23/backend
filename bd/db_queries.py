'''тут функции для обращения к БД'''

from datetime import datetime
from bd.models import db, News, Users

import weedly_app
app = weedly_app.create_app()

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
    with app.app_context():
        for article in data:
           # проверили, что ссылка и автор уникальны. (у одной статьи может быть несколько авторов)
            existing = News.query.filter(News.url == article['link']).filter(News.author == article['author']).count()
            if not existing:
                new = News(title = article['title'], author=article['author'],url=article['link'],
                           source_name=article['source_name'],published = datetime(*article['publication_date_parsed'][:5]))
                db.session.add(new)
                db.session.commit()
                print('добавили в БД:', article['title'])


def get_latest_news(how_many = 3):
    '''отдает последние новости в виде списка объектов models.News.
        атрибуты (заголовок, ссылка и тд) можно получить через точку.
    '''
    with app.app_context():
        news = db.session.query(News).order_by(News.published.desc())[:how_many]
        return news



# import json
# file = '../kommersant.json'
# file2 = '../meduza.json'
# files = [file, file2]
# list_to_add = []
# for file in files:
#     with open(file,'r', encoding='utf-8') as f:
#         data = json.load(f)['norm authors']
#         for e in data:
#             list_to_add.append(e)
#
# add_news(list_to_add)
#
