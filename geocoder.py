import requests

def search_object(query, api_key):
    if not query or not api_key:
        return None

    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": api_key,
        "geocode": query,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None

        data = response.json()
        feature_member = data['response']['GeoObjectCollection']['featureMember']
        if not feature_member:
            return None

        first = feature_member[0]
        pos = first['GeoObject']['Point']['pos']
        lon, lat = map(float, pos.split())
        return lon, lat
    except Exception:
        return None