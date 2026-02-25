import os
from dotenv import load_dotenv

load_dotenv()

GEOCODER_API_KEY = os.getenv("GEOCODER_APIKEY")
STATIC_API_KEY = os.getenv("STATIC_MAPS_APIKEY")

DEFAULT_LAT = 55.7558
DEFAULT_LON = 37.6176
DEFAULT_ZOOM = 12