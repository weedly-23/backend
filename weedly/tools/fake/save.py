import csv
import time
from pathlib import Path

from weedly.db.db import db_session
from weedly.db.model import Articles


def from_csv(filepath: Path):
    with open(filepath, 'r', encoding='utf-8') as f:
        fields = [
            "title",
            "author",
            "url",
            "source_name",
            "published"
        ]
        reader = csv.DictReader(f, fields, delimiter=';')
        return [row for row in reader]


def save_data(filepath: Path):
    data = from_csv(filepath)
    db_session.bulk_insert_mappings(Articles, data)
    db_session.commit()


if __name__ == "__main__":
    start = time.time()
    filepath = Path('.data') / 'fake' / 'fakenews.csv'
    save_data(filepath)
    print(f"Загрузка заняла: {time.time() -  start} секунд.")
