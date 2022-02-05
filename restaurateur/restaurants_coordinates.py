import requests

from datetime import datetime
from dotenv import load_dotenv
from geopy import distance
from annoying.functions import get_object_or_None

from coordinates.models import Coordinates



def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection'][
        'featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def calculate_distance(restaurant, order, apikey):
    coordinates = get_object_or_None(Coordinates, address=order)
    if not coordinates:
        restaurant_coords = restaurant.lat, restaurant.lon
        order_lon, order_lat = fetch_coordinates(apikey, order)
        order_coords = order_lat, order_lon
        if order_coords is None:
            order_distance_km = 'check the coordinates'
            return order_distance_km

        Coordinates.objects.create(
            launch_geocoder_date=datetime.now(),
            address=order,
            lat=order_lat,
            lon=order_lon,
        )
    else:
        restaurant_coords = restaurant.lat, restaurant.lon
        order_coords = coordinates.lat, coordinates.lon

    order_distance_km = round(
        distance.distance(restaurant_coords, order_coords).km, 3)
    return order_distance_km
