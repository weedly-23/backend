# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True \
    POETRY_VIRTUALENVS_CREATE=False

WORKDIR /app
EXPOSE 5000

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev

COPY weedly /app/weedly

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "weedly.app:app"]
