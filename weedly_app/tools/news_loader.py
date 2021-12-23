'''загрузить тестовый набор новостей в нашем формате'''

import json
from typing import Any


def get_test_news_for_db()-> list[dict[str, Any]]:
    '''загружает тестовые новости для ДБ'''
    file = 'data/kommersant.json'
    file2 = 'data/meduza.json'
    files = [file, file2]
    print('files---',files)
    results = []
    for file in files:
        with open(file,'r', encoding='utf-8') as f:
            data = json.load(f)['norm authors']
            results.append(data)

    return sum(results,[])


def get_news_from_file(file):
    '''загружается новости'''
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)['norm authors']
        return data

