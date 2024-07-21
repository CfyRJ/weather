
# Weather

### Weather is a project that displays weather using an API: https://open-meteo.com/.
### May:
* Embrace the city in any language and a little more.
* Show address. Weather. Temperature in degrees Celsius. Wind speed in m/s.
* Prompt which city was entered last and suggest it.
* Show request history.
* Show how many times you entered which city.

## Install

### Prepare the database.

### Before installing the application, prepare your environment variables:
* DATABASE_URL - [variable for connecting to the database.](https://ru.hexlet.io/blog/posts/python-postgresql)
* SECRET_KEY

### After cloning from GitHub, run the commands:
* make build
* make start

### After cloning from GitHub, run the commands:
* The project deployment has not been tested. To test functionality in DEBUG mode, use the standard:
`python manage.py runserver`


### Для проверяющих по ТЗ из O-complex.
* Написаны тесты, можно вызвать как `make test`
* Чистота кода проверена с помощью flake8, можно вызвать как `make lint`
* Сделано при повторном посещении сайта будет предложено посмотреть погоду в городе, в котором пользователь уже смотрел ранее (на основной странице) (с помощью сессий)
* Сделано история поиска для каждого пользователя (на основной странице) (с помощью сессий)
* Сделана страница (можно быстро и легко переделать под API и json), показывающая сколько раз вводили какой город (на странице: /count_cities/)
