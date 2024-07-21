import openmeteo_requests

import requests_cache
from retry_requests import retry
import datetime


WEATHER_CODE = {
    0: 'Чистое небо',
    1: 'В основном ясно',
    2: 'Переменная облачность',
    3: 'Облачно',
    45: 'Туман',
    48: 'Иней',
    51: 'Слабая морось',
    53: 'Морось',
    55: 'Сильная морось',
    56: 'Слабый мокрый снег',
    57: 'Мокрый снег',
    61: 'Небольшой дождь',
    63: 'Умеренный дождь',
    65: 'Ливень',
    66: 'Слабый ледяной дождь',
    67: 'Сильный ледяной дождь',
    71: 'Слабый снег',
    73: 'Снег',
    75: 'Сильный снег',
    77: 'Буран',
    80: 'Слабый ливень',
    81: 'Ливень',
    82: 'Сильный ливень',
    85: 'Слабый снег',
    86: 'Сильный снегопад',
    95: 'Слабая гроза',
    96: 'Гроза',
    99: 'гроза с градом',
}


def get_weather(latitude, longitude) -> dict:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important
    # to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "weather_code", "wind_speed_10m"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple
    # locations or weather models
    response = responses[0]

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_weather_code = current.Variables(1).Value()
    current_wind_speed_10m = current.Variables(2).Value()

    return {
        'time': datetime.datetime.fromtimestamp(current.Time()),
        'temperature': round(current_temperature_2m, 3),
        'weather': WEATHER_CODE[current_weather_code],
        'wind': round(current_wind_speed_10m, 3),
    }
