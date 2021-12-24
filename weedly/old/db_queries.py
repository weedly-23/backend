from typing import Any

from weedly.db.model import db, News
import arrow


class NewsRepo:

    def add_news(self, data: list[dict[str, Any]]):
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
                published = arrow.get(*article['published'][:-2]).datetime

            elif isinstance(article['published'],str):
                published = arrow.get(article['published'],'DD MMM YYYY HH:mm:ss').datetime

            else:
                print('неправильный формат даты---', article['published'])

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

    def get_latest_news(self, how_many = 3):
        '''
        отдает последние новости в виде списка объектов models.News.
        атрибуты (заголовок, ссылка и тд) можно получить через точку.
        '''
        news = db.session.query(News).order_by(News.published.desc())[:how_many]
        return news
