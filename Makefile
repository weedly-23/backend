lint:
	@mypy weedly_app
	@flake8 weedly_app

test:
	@pytest

dev.install:
	@pip install -r requirements.txt
