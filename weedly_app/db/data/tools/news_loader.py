'''загрузить тестовый набор новостей в нашем формате'''

import json

def get_test_news_for_db()-> list:
    '''загружает тестовые новости для ДБ'''
    file = 'weedly_app/db/kommersant.json'
    file2 = 'weedly_app/db/meduza.json'
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

