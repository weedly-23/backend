# Бэкэнд с БД на Sqlite

## Создание БД

Создать пустую локальную БД:

```bash
make db.recreate
```

Добавить в таблицу с новостями фейк-новости:

```bash
make db.fake.save
```

Удалить все из БД:

```bash
make clean
```

## Запуск сервера

В `weedly/app.py` создается приложение.
Сервер запускается из `__main__.py` командой `make run`.

## Deployment

```bash
git checkout main
git pull

docker-compose down
docker-compose up -d db
docker-compose run weedly-app python -m weedly.db.model
docker-compose up -d weedly-app

docker-compose logs --tail 10 -f weedly-app
```

## Usage

Add some news:

```bash
curl --request POST \
  --url http://localhost:5000/api/v1/feeds/ \
  --header 'Content-Type: application/json' \
  --data '{
        "title": "интересная новость",
        "author": "иванов",
        "url": "http://ya.ru",
        "source_name": "rbc",
        "published": "2020-02-02"
    }'
```

Get all news:

```bash
curl --request GET \
  --url http://localhost:5000/api/v1/feeds/
```
