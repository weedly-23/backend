import csv
import time

from weedly_app.db.db import db_session
from weedly_app.db.model import News


def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = [
            "title",
            "author",
            "url",
            "source_name",
            "published"
        ]
        reader = csv.DictReader(f, fields, delimiter=';')
        data = [row for row in reader]
        _save_data(data)


def _save_data(data):
    db_session.bulk_insert_mappings(News, data)
    db_session.commit()


if __name__ == "__main__":
    start = time.time()
    read_csv("fakenews.csv")
    print(f"Загрузка заняла: {time.time() -  start} секунд.")