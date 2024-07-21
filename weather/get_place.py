from geopy.geocoders import Nominatim
import logging


def get_place(place: str) -> dict:

    geolocator = Nominatim(user_agent="Weather_CfyRJ")
    location = geolocator.geocode(place)

    if location is None:
        logging.info('City not find')
        return None

    logging.info('City is find')

    return {
        'address': location.address,
        'latitude': location.latitude,
        'longitude': location.longitude,
    }
