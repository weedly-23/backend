# Бэкэнд с БД на Sqlite

## API методы

Добавить новый feed (пока ручками из апишки):

```bash
curl --request POST \
     --url http://localhost:5000/api/v1/feeds/ \
     --header 'Content-Type: application/json' \
     --data '{
            "name": "медуза: IT",
            "category": "it news",
            "url": "http://meduza.ru",
            "is_rss": true
        }'
```

Получить список feed для rss parser'а:

```bash
curl --request GET \
     --url http://localhost:5000/api/v1/feeds/
```

Добавить авторов в feed:

```bash
curl --request POST \
  --url http://localhost:5000/api/v1/authors/ \
  --header 'Content-Type: application/json' \
  --data '{
        "name": "vladimir 6",
        "feed_id": 1
    }'
```

Получить всех авторов feed:

```bash
curl --request GET \
     --url http://localhost:5000/api/v1/feeds/1/authors/
```

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

## Swagger Api Docs

```text
## get all media resources
GET /api/v1/media/

## get media info
GET /api/v1/media/{uid}

## get media feeds
GET /api/v1/media/{uid}/feeds/
[rss1, rss2]

## get all media authors
GET /api/v1/media/{uid}/authors/

## get articles for each authors
GET /api/v1/authors/{uid}/articles/

## get authors rating
GET /api/v1/authors/{uid}/rating

## get authors
GET /api/v1/authors/{uid}

## get articles from user best authors
GET /api/v1/users/{uid}/articles/

# First priority

## get articles from media feed
GET /api/v1/feeds/{rss-id}/articles/

## get feeds for rss parser
GET /api/v1/feeds/?title=hacker&category=it
title='Hackernews'
category='IT'
rss_url='rss://'
where not is_deleted

## add any rss feed for adminstrators
POST /api/v1/feeds/

DELETE /api/v1/feeds/{uid} for adminstrators
is_deleted

## get articles from
GET /api/v1/feeds/{uid}/articles/
```

1 stage:
/feeds -> /articles
model.news -> articles
model.feeds with title, rss, category (index)
model.users -> feeds
model.articles -> feeds

```http
POST /api/v1/feeds/
POST /api/v1/articles/

GET /api/v1/feeds/?title=hacker&category=it
DELETE /api/v1/articles/{uid}  # is_deleted
```

2 stage:
add users with user feeds

3 stage:
async notifications from my best feeds

4 stage:
add media

## Что сделано

1. связанные таблицы `Feed`, `Users`, `Author`, `Article`.
2. классы для обращения к БД - загрузка (DataLoader) и извлечение (DataGetter)
в db_funs.py можно наполнить БД данными из тестовых rss-потоков
3. rss-парсер лежит в utils
