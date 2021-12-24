# syntax=docker/dockerfile:1
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=True

WORKDIR /app
EXPOSE 5000

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY data /app/data
COPY weedly_app /app/weedly_app

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
