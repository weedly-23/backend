# Бэкэнд с БД на Sqlite

## Создание БД
В папке db.models прописаны модели (таблицы). 
News соответствует формату, который отдают наши парсеры.

Создать пустую локальную БД:

 
python -m weedly_app.db.create_news_db create-db 


Добавить в таблицу с новостями новости из json файла:

python -m weedly_app.db.create_db add-news-from-file "file path"

Создать локальную БД с тестовыми данными:

python -m weedly_app.db.create_news_db create-db --fill-with-data

В нее сразу загрузятся 80 тестовых новостей из .json, которые лежат рядом (загрузчик новостей лежит в tools). 

В db_queries лежат функции для загрузки и получения данных из БД.

Путь для БД прописан в config.py

Удалить все из БД
python -m weedly_app.db.create_db reset-news-table


## Запуск сервера
В weedly_app/app.py создается приложение. Сервер запускается из __main__.py командой python -m weedly_app




