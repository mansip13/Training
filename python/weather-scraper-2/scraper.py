"""
WORKING Weather scraper for timeanddate.com
Fixed to match actual HTML structure of timeanddate.com
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from dataclasses import dataclass
import pendulum

console = Console()

@dataclass
class WeatherData:
    """Simple weather data class"""
    location: str
    country: str
    city: str
    current_temp: str
    condition: str
    feels_like: Optional[str] = None
    humidity: Optional[str] = None
    wind: Optional[str] = None
    pressure: Optional[str] = None
    visibility: Optional[str] = None
    forecast_high_low: Optional[str] = None
    hourly_forecast: List[Dict] = None
    timestamp: str = ""

    def __post_init__(self):
        if self.hourly_forecast is None:
            self.hourly_forecast = []
        if not self.timestamp:
            self.timestamp = pendulum.now().to_iso8601_string()

class WeatherScraper:
    """WORKING weather scraper with proper parsing"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def parse_location_input(self, location_input: str) -> Tuple[str, str]:
        """Parse COUNTRY/CITY format ONLY"""
        if '/' not in location_input:
            raise ValueError("Please use Country/City format (e.g., 'Japan/Tokyo')")

        parts = location_input.split('/')
        if len(parts) != 2:
            raise ValueError("Please use Country/City format (e.g., 'Japan/Tokyo')")

        country = parts[0].strip()
        city = parts[1].strip()

        if not country or not city:
            raise ValueError("Both country and city are required (e.g., 'Japan/Tokyo')")

        return city, country

    def _clean_name(self, name: str) -> str:
        """Clean name for URL"""
        return name.lower().replace(' ', '-').replace('_', '-')

    def get_weather_by_location(self, location_input: str) -> Optional[WeatherData]:
        """Get weather data with FIXED parsing"""
        try:
            # Parse input - MUST be Country/City format
            city, country = self.parse_location_input(location_input)

            # Clean names for URL
            country_clean = self._clean_name(country)
            city_clean = self._clean_name(city)

            # Construct URL
            url = f"https://www.timeanddate.com/weather/{country_clean}/{city_clean}"
            console.print(f"🔗 URL: {url}")

            # Get page
            response = self.session.get(url, timeout=15)
            console.print(f"📡 Status: {response.status_code}")

            if response.status_code != 200:
                console.print(f"❌ Failed to get page: {response.status_code}")
                return None

            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Check if we got the right page
            page_text = soup.get_text()
            console.print(f"📄 Page contains 'weather': {'weather' in page_text.lower()}")
            console.print(f"📄 Page contains '°F': {'°F' in page_text}")

            # Debug: Print first 500 characters to see what we got
            console.print(f"📄 First 500 chars: {page_text[:500]}")

            if 'weather' not in page_text.lower():
                console.print("❌ Page does not contain weather data")
                return None

            # Extract weather data using IMPROVED methods
            current_temp = self._extract_temperature(soup, page_text)
            condition = self._extract_condition(soup, page_text)
            feels_like = self._extract_feels_like(page_text)
            forecast_range = self._extract_forecast(page_text)
            humidity = self._extract_humidity(page_text)
            wind = self._extract_wind(page_text)
            pressure = self._extract_pressure(page_text)
            visibility = self._extract_visibility(page_text)

            console.print(f"🌡️ Found temp: {current_temp}")
            console.print(f"☁️ Found condition: {condition}")
            console.print(f"🌡️ Found feels like: {feels_like}")

            if current_temp == "N/A":
                console.print("❌ No temperature found - printing more debug info")
                # Find all temperature-like patterns
                temp_patterns = re.findall(r'\d+\s*°F', page_text)
                console.print(f"🔍 Found temperature patterns: {temp_patterns[:10]}")
                return None

            # Get hourly data
            hourly_data = self._get_hourly_forecast(country_clean, city_clean)

            return WeatherData(
                location=f"{city}, {country}",
                country=country,
                city=city,
                current_temp=current_temp,
                condition=condition,
                feels_like=feels_like,
                humidity=humidity,
                wind=wind,
                pressure=pressure,
                visibility=visibility,
                forecast_high_low=forecast_range,
                hourly_forecast=hourly_data
            )

        except ValueError as e:
            console.print(f"❌ Input error: {str(e)}", style="red")
            return None
        except Exception as e:
            console.print(f"❌ Error: {str(e)}", style="red")
            return None

    def _extract_temperature(self, soup: BeautifulSoup, text: str) -> str:
        """Extract current temperature with MULTIPLE strategies"""

        # Strategy 1: Look for "Now" followed by temperature
        now_pattern = re.search(r'Now\s*[\n\r]*\s*(\d+)\s*°F', text, re.IGNORECASE | re.MULTILINE)
        if now_pattern:
            temp_f = int(now_pattern.group(1))
            temp_c = (temp_f - 32) * 5/9
            console.print(f"🎯 Found temp with 'Now' pattern: {temp_f}°F")
            return f"{temp_c:.0f}°C"

        # Strategy 2: Look for first large temperature in the page
        all_temps = re.findall(r'(\d+)\s*°F', text)
        if all_temps:
            for temp_str in all_temps:
                temp_f = int(temp_str)
                if 30 <= temp_f <= 120:  # Reasonable current temperature range
                    temp_c = (temp_f - 32) * 5/9
                    console.print(f"🎯 Found temp with general pattern: {temp_f}°F")
                    return f"{temp_c:.0f}°C"

        # Strategy 3: Look in specific HTML elements
        # Try to find temperature in h2, div, span tags
        for tag in ['h2', 'h3', 'div', 'span']:
            elements = soup.find_all(tag)
            for element in elements:
                element_text = element.get_text()
                temp_match = re.search(r'(\d+)\s*°F', element_text)
                if temp_match:
                    temp_f = int(temp_match.group(1))
                    if 30 <= temp_f <= 120:
                        temp_c = (temp_f - 32) * 5/9
                        console.print(f"🎯 Found temp in {tag} element: {temp_f}°F")
                        return f"{temp_c:.0f}°C"

        console.print("❌ No temperature found with any strategy")
        return "N/A"

    def _extract_condition(self, soup: BeautifulSoup, text: str) -> str:
        """Extract weather condition with multiple strategies"""

        # Common weather conditions from timeanddate.com
        conditions = [
            'Passing clouds', 'Clear', 'Sunny', 'Cloudy', 'Partly cloudy',
            'Overcast', 'Rain', 'Snow', 'Thunderstorm', 'Fog', 'Mist',
            'Broken clouds', 'Scattered clouds', 'Mostly sunny', 'Mostly cloudy',
            'Light rain', 'Heavy rain', 'Drizzle', 'Showers', 'Fair'
        ]

        # Strategy 1: Look for conditions after temperature
        temp_areas = re.findall(r'\d+\s*°F[\s\n\r]([^\n\r]{1,30})', text)
        for area in temp_areas:
            for condition in conditions:
                if condition in area:
                    console.print(f"🎯 Found condition after temp: {condition}")
                    return condition

        # Strategy 2: Look anywhere in text
        for condition in conditions:
            if condition in text:
                console.print(f"🎯 Found condition in text: {condition}")
                return condition

        # Strategy 3: Look for condition patterns
        condition_patterns = [
            r'([A-Z][a-z]+ [a-z]+)\.', # "Passing clouds."
            r'\d+\s*°F[\s\n\r]*([A-Z][a-z ]+)\.',  # After temperature
        ]

        for pattern in condition_patterns:
            match = re.search(pattern, text)
            if match:
                potential_condition = match.group(1).strip()
                if len(potential_condition) < 30:  # Reasonable length
                    console.print(f"🎯 Found condition with pattern: {potential_condition}")
                    return potential_condition

        return "N/A"

    def _extract_feels_like(self, text: str) -> Optional[str]:
        """Extract feels like temperature"""
        match = re.search(r'Feels Like[:\s]+(\d+)\s*°F', text, re.IGNORECASE)
        if match:
            temp_f = int(match.group(1))
            temp_c = (temp_f - 32) * 5/9
            return f"{temp_c:.0f}°C"
        return None

    def _extract_forecast(self, text: str) -> Optional[str]:
        """Extract forecast high/low"""
        match = re.search(r'Forecast[:\s]+(\d+)\s*/\s*(\d+)\s*°F', text, re.IGNORECASE)
        if match:
            high_f = int(match.group(1))
            low_f = int(match.group(2))
            high_c = (high_f - 32) * 5/9
            low_c = (low_f - 32) * 5/9
            return f"{high_c:.0f} / {low_c:.0f}°C"
        return None

    def _extract_humidity(self, text: str) -> Optional[str]:
        """Extract humidity"""
        match = re.search(r'Humidity[:\s]+(\d+%)', text, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_wind(self, text: str) -> Optional[str]:
        """Extract wind information"""
        match = re.search(r'Wind[:\s]+([^\n\r]{1,50})', text, re.IGNORECASE)
        if match:
            wind = match.group(1).strip()
            # Clean up wind string
            wind = re.sub(r'\s+', ' ', wind)
            return wind if len(wind) < 50 else wind[:47] + "..."
        return None

    def _extract_pressure(self, text: str) -> Optional[str]:
        """Extract pressure"""
        match = re.search(r'Pressure[:\s]+([\d\.]+ "Hg)', text, re.IGNORECASE)
        return match.group(1) if match else None

    def _extract_visibility(self, text: str) -> Optional[str]:
        """Extract visibility"""
        match = re.search(r'Visibility[:\s]+([^\n\r]{1,20})', text, re.IGNORECASE)
        if match:
            visibility = match.group(1).strip()
            return visibility if visibility != "N/A" and len(visibility) < 20 else None
        return None

    def _get_hourly_forecast(self, country: str, city: str) -> List[Dict]:
        """Get hourly forecast data"""
        try:
            url = f"https://www.timeanddate.com/weather/{country}/{city}/hourly"
            console.print(f"🕐 Getting hourly: {url}")

            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                console.print(f"⚠️ Hourly page status: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            hourly_data = []

            # Look for hourly data in tables
            tables = soup.find_all('table')
            console.print(f"📊 Found {len(tables)} tables on hourly page")

            for i, table in enumerate(tables):
                rows = table.find_all('tr')
                console.print(f"📊 Table {i+1} has {len(rows)} rows")

                for row_idx, row in enumerate(rows):
                    cells = row.find_all(['td', 'th'])

                    if len(cells) >= 3:
                        time_cell = cells[0].get_text(strip=True)
                        temp_cell = cells[1].get_text(strip=True)
                        condition_cell = cells[2].get_text(strip=True)

                        # Check if this looks like hourly data
                        if re.search(r'\d{1,2}:\d{2}\s*(am|pm)', time_cell, re.IGNORECASE):
                            # Extract temperature
                            temp_match = re.search(r'(\d+)\s*°F', temp_cell)
                            if temp_match:
                                temp_f = int(temp_match.group(1))
                                temp_c = (temp_f - 32) * 5/9

                                formatted_time = self._format_time(time_cell)

                                hourly_data.append({
                                    'time': formatted_time,
                                    'temperature': f"{temp_c:.0f}°C",
                                    'condition': condition_cell[:25]  # Limit length
                                })

                                console.print(f"📊 Added hourly data: {formatted_time} - {temp_c:.0f}°C")

                if len(hourly_data) >= 5:  # Found good data
                    break

            console.print(f"📊 Total hourly data points: {len(hourly_data)}")
            return hourly_data[:24]  # Max 24 hours

        except Exception as e:
            console.print(f"⚠️ Hourly data error: {str(e)}")
            return []

    def _format_time(self, time_text: str) -> str:
        """Format time to HH:MM"""
        match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)', time_text, re.IGNORECASE)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            am_pm = match.group(3).lower()

            if am_pm == 'pm' and hour != 12:
                hour += 12
            elif am_pm == 'am' and hour == 12:
                hour = 0

            return f"{hour:02d}:{minute:02d}"

        return time_text

    def close(self):
        """Close session"""
        self.session.close()
