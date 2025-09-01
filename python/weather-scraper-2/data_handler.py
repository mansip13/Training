"""
Data handling functionality for saving and loading weather data
Supports JSON and CSV formats with proper file naming
"""

import json
import csv
import os
import pandas as pd
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from pathlib import Path
import pendulum
from dataclasses import asdict

from config import FILE_PATTERNS
from scraper import WeatherData

console = Console()

class DataHandler:
    """Handles saving and loading of weather data"""

    def __init__(self):
        self.data_dir = Path("weather_data")
        self.data_dir.mkdir(exist_ok=True)

    def generate_filename(self, weather_data: WeatherData, file_format: str) -> str:
        """
        Generate filename based on location and format

        Args:
            weather_data: Weather data object
            file_format: 'json' or 'csv'

        Returns:
            Generated filename
        """
        # Clean city and country names for filename
        city = self._clean_filename(weather_data.city)
        country = self._clean_filename(weather_data.country)

        pattern = FILE_PATTERNS[file_format]
        filename = pattern.format(country=country, city=city)

        return str(self.data_dir / filename)

    def _clean_filename(self, name: str) -> str:
        """Clean name for use in filename"""
        import re
        # Remove special characters and replace spaces with hyphens
        cleaned = re.sub(r'[^\w\s-]', '', name)
        cleaned = re.sub(r'[-\s]+', '-', cleaned)
        return cleaned.strip('-').lower()

    def save_json(self, weather_data: WeatherData, filename: Optional[str] = None) -> bool:
        """
        Save weather data to JSON file

        Args:
            weather_data: Weather data to save
            filename: Optional custom filename

        Returns:
            True if successful, False otherwise
        """
        try:
            if filename is None:
                filename = self.generate_filename(weather_data, 'json')

            # Convert dataclass to dictionary
            data_dict = asdict(weather_data)

            # Add metadata
            data_dict['metadata'] = {
                'saved_at': pendulum.now().to_iso8601_string(),
                'data_version': '1.0',
                'source': 'timeanddate.com'
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, indent=2, ensure_ascii=False)

            console.print(f"✅ Weather data saved to: [bold green]{filename}[/bold green]")
            return True

        except Exception as e:
            console.print(f"❌ Error saving JSON file: {str(e)}", style="red")
            return False

    def save_csv(self, weather_data: WeatherData, filename: Optional[str] = None) -> bool:
        """
        Save weather data to CSV file

        Args:
            weather_data: Weather data to save
            filename: Optional custom filename

        Returns:
            True if successful, False otherwise
        """
        try:
            if filename is None:
                filename = self.generate_filename(weather_data, 'csv')

            # Prepare data for CSV
            csv_data = []

            # Basic weather information
            basic_info = {
                'Type': 'Current Weather',
                'Location': weather_data.location,
                'City': weather_data.city,
                'Country': weather_data.country,
                'Temperature': weather_data.current_temp,
                'Condition': weather_data.condition,
                'Humidity': weather_data.humidity or 'N/A',
                'Wind': weather_data.wind or 'N/A',
                'Pressure': weather_data.pressure or 'N/A',
                'Visibility': weather_data.visibility or 'N/A',
                'UV Index': weather_data.uv_index or 'N/A',
                'Timestamp': weather_data.timestamp,
                'Time': '',
                'Notes': ''
            }
            csv_data.append(basic_info)

            # Hourly forecast data
            for i, hour_data in enumerate(weather_data.hourly_forecast):
                hourly_info = {
                    'Type': 'Hourly Forecast',
                    'Location': weather_data.location,
                    'City': weather_data.city,
                    'Country': weather_data.country,
                    'Temperature': hour_data.get('temperature', 'N/A'),
                    'Condition': hour_data.get('condition', 'N/A'),
                    'Humidity': 'N/A',
                    'Wind': 'N/A',
                    'Pressure': 'N/A',
                    'Visibility': 'N/A',
                    'UV Index': 'N/A',
                    'Timestamp': weather_data.timestamp,
                    'Time': hour_data.get('time', f'Hour {i+1}'),
                    'Notes': 'Forecast data'
                }
                csv_data.append(hourly_info)

            # Write to CSV
            if csv_data:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                    writer.writeheader()
                    writer.writerows(csv_data)

                console.print(f"✅ Weather data saved to: [bold green]{filename}[/bold green]")
                return True
            else:
                console.print("❌ No data to save to CSV", style="red")
                return False

        except Exception as e:
            console.print(f"❌ Error saving CSV file: {str(e)}", style="red")
            return False

    def load_json(self, filename: str) -> Optional[WeatherData]:
        """
        Load weather data from JSON file

        Args:
            filename: Path to JSON file

        Returns:
            WeatherData object or None if loading fails
        """
        try:
            if not os.path.exists(filename):
                console.print(f"❌ File not found: {filename}", style="red")
                return None

            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Remove metadata before creating WeatherData object
            if 'metadata' in data:
                del data['metadata']

            # Create WeatherData object
            weather_data = WeatherData(**data)

            console.print(f"✅ Weather data loaded from: [bold green]{filename}[/bold green]")
            return weather_data

        except Exception as e:
            console.print(f"❌ Error loading JSON file: {str(e)}", style="red")
            return None

    def load_csv_as_dataframe(self, filename: str) -> Optional[pd.DataFrame]:
        """
        Load CSV file as pandas DataFrame

        Args:
            filename: Path to CSV file

        Returns:
            Pandas DataFrame or None if loading fails
        """
        try:
            if not os.path.exists(filename):
                console.print(f"❌ File not found: {filename}", style="red")
                return None

            df = pd.read_csv(filename)
            console.print(f"✅ CSV data loaded from: [bold green]{filename}[/bold green]")
            return df

        except Exception as e:
            console.print(f"❌ Error loading CSV file: {str(e)}", style="red")
            return None

    def list_saved_files(self) -> Dict[str, List[str]]:
        """
        List all saved weather data files

        Returns:
            Dictionary with 'json' and 'csv' keys containing file lists
        """
        json_files = list(self.data_dir.glob("*.json"))
        csv_files = list(self.data_dir.glob("*.csv"))

        return {
            'json': [str(f) for f in json_files],
            'csv': [str(f) for f in csv_files]
        }

    def display_saved_files(self):
        """Display saved files in a formatted table"""
        files = self.list_saved_files()

        if not files['json'] and not files['csv']:
            console.print("📁 No saved weather data files found.", style="yellow")
            return

        table = Table(title="Saved Weather Data Files")
        table.add_column("Format", style="cyan")
        table.add_column("Filename", style="green")
        table.add_column("Size", style="yellow")
        table.add_column("Modified", style="blue")

        for json_file in files['json']:
            file_path = Path(json_file)
            if file_path.exists():
                size = self._format_file_size(file_path.stat().st_size)
                modified = pendulum.from_timestamp(file_path.stat().st_mtime).format('YYYY-MM-DD HH:mm')
                table.add_row("JSON", file_path.name, size, modified)

        for csv_file in files['csv']:
            file_path = Path(csv_file)
            if file_path.exists():
                size = self._format_file_size(file_path.stat().st_size)
                modified = pendulum.from_timestamp(file_path.stat().st_mtime).format('YYYY-MM-DD HH:mm')
                table.add_row("CSV", file_path.name, size, modified)

        console.print(table)

    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"

    def interactive_save(self, weather_data: WeatherData) -> bool:
        """
        Interactive save dialog with format selection

        Args:
            weather_data: Weather data to save

        Returns:
            True if saved successfully, False otherwise
        """
        console.print("\n💾 Save Weather Data", style="bold cyan")

        # Show current data summary
        self._display_data_summary(weather_data)

        # Ask for format
        format_choice = Prompt.ask(
            "Choose format",
            choices=["json", "csv", "both"],
            default="json"
        )

        # Ask for custom filename
        use_custom = Confirm.ask("Use custom filename?", default=False)

        success = True

        if format_choice in ["json", "both"]:
            filename = None
            if use_custom:
                default_json = self.generate_filename(weather_data, 'json')
                filename = Prompt.ask(f"JSON filename", default=Path(default_json).name)
                filename = str(self.data_dir / filename)
                if not filename.endswith('.json'):
                    filename += '.json'

            success &= self.save_json(weather_data, filename)

        if format_choice in ["csv", "both"]:
            filename = None
            if use_custom:
                default_csv = self.generate_filename(weather_data, 'csv')
                filename = Prompt.ask(f"CSV filename", default=Path(default_csv).name)
                filename = str(self.data_dir / filename)
                if not filename.endswith('.csv'):
                    filename += '.csv'

            success &= self.save_csv(weather_data, filename)

        return success

    def _display_data_summary(self, weather_data: WeatherData):
        """Display summary of weather data to be saved"""
        table = Table(title="Weather Data Summary")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Location", weather_data.location)
        table.add_row("Temperature", weather_data.current_temp)
        table.add_row("Condition", weather_data.condition)
        table.add_row("Hourly Forecast Points", str(len(weather_data.hourly_forecast)))
        table.add_row("Timestamp", pendulum.parse(weather_data.timestamp).format('YYYY-MM-DD HH:mm:ss'))

        console.print(table)

    def export_to_pandas(self, weather_data: WeatherData) -> pd.DataFrame:
        """
        Convert weather data to pandas DataFrame for analysis

        Args:
            weather_data: Weather data to convert

        Returns:
            Pandas DataFrame
        """
        # Prepare data for DataFrame
        data_rows = []

        # Add current weather
        current_row = {
            'datetime': pendulum.parse(weather_data.timestamp),
            'location': weather_data.location,
            'city': weather_data.city,
            'country': weather_data.country,
            'temperature_str': weather_data.current_temp,
            'temperature_numeric': self._extract_temperature_value(weather_data.current_temp),
            'condition': weather_data.condition,
            'humidity': weather_data.humidity,
            'wind': weather_data.wind,
            'pressure': weather_data.pressure,
            'type': 'current'
        }
        data_rows.append(current_row)

        # Add hourly forecast
        for hour_data in weather_data.hourly_forecast:
            hourly_row = {
                'datetime': None,  # Would need to parse time
                'location': weather_data.location,
                'city': weather_data.city,
                'country': weather_data.country,
                'temperature_str': hour_data.get('temperature', ''),
                'temperature_numeric': self._extract_temperature_value(hour_data.get('temperature', '')),
                'condition': hour_data.get('condition', ''),
                'humidity': None,
                'wind': None,
                'pressure': None,
                'type': 'forecast',
                'forecast_time': hour_data.get('time', '')
            }
            data_rows.append(hourly_row)

        return pd.DataFrame(data_rows)

    def _extract_temperature_value(self, temp_str: str) -> Optional[float]:
        """Extract numeric temperature value from string"""
        import re

        if not temp_str:
            return None

        match = re.search(r'(-?\d+(?:\.\d+)?)', temp_str)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None

        return None
