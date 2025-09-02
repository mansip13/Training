"""Configuration and constants for the Weather CLI app."""

import os

# File templates
CITIES_FILE_TEMPLATE = "{}_cities.json"

# URLs
BASE_URL = "https://www.timeanddate.com/weather"
COUNTRY_URL_TEMPLATE = "https://www.timeanddate.com/weather/{}"
CITY_URL_TEMPLATE = "https://www.timeanddate.com/weather/{}/{}"
HISTORIC_URL_TEMPLATE = "https://www.timeanddate.com/weather/{}/{}/historic?hd={}"

# Request settings
REQUEST_TIMEOUT = 20
REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# File settings
DATA_DIR = "weather_data"
DEFAULT_COUNTRY = "india"

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)