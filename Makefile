-include .env
export


lint:
	@mypy weedly
	@flake8 weedly


test:
	@pytest


dev.install:
	@pip install -r requirements.txt


db.up:
	@docker-compose up -d db


db.recreate: db.clean db.up
	@sleep 5
	@python -m weedly.db


db.clean:
	@echo "clean all resources: db"
	@docker-compose down -t1


run:
	@python -m weedly
