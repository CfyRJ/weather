install:
	poetry install

start_debug:
	poetry run python manage.py runserver

# start:
# 	gunicorn weaather.wsgi:application

test:
	poetry run python manage.py test

lint:
	poetry run flake8 weather

# build:
# 	./build.sh
