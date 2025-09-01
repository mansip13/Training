"""
Configuration file for Weather CLI Scraper
Contains constants, URLs, and configuration settings
"""

# Base URLs
BASE_URL = "https://www.timeanddate.com"
WEATHER_URL = "https://www.timeanddate.com/weather"
SEARCH_URL = "https://www.timeanddate.com/weather"

# HTTP Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# File naming patterns
FILE_PATTERNS = {
    'json': '{country}-{city}.json',
    'csv': '{country}-{city}.csv'
}

# Chart settings
CHART_HEIGHT = 15
CHART_WIDTH = 80
TEMPERATURE_COLORS = {
    'cold': 'blue',
    'mild': 'green', 
    'warm': 'yellow',
    'hot': 'red'
}

# Date formats
DATE_FORMATS = {
    'input': ['YYYY-MM-DD', 'MM/DD/YYYY', 'DD/MM/YYYY'],
    'display': 'MMMM DD, YYYY',
    'filename': 'YYYY-MM-DD'
}

# Time points for date range queries
TIME_POINTS = ['06:00', '12:00', '18:00', '00:00']

# Menu options
MENU_OPTIONS = {
    '1': 'Search weather by city/country',
    '2': 'View hourly forecast for today',
    '3': 'Save weather data (JSON/CSV)',
    '4': 'Filter 24-hour data by date',
    '5': 'Date range temperature query',
    '6': 'Exit'
}

# Temperature thresholds (Fahrenheit)
TEMP_THRESHOLDS = {
    'cold': 50,
    'mild': 70,
    'warm': 85,
    'hot': 100
}

# Default settings
DEFAULT_SETTINGS = {
    'temperature_unit': 'fahrenheit',
    'date_format': 'YYYY-MM-DD',
    'chart_height': 15,
    'auto_save': False
}