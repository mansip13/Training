"""
Weather display functionality using rich for beautiful CLI output
Handles formatting and presentation of real weather data
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.align import Align
from typing import List, Dict, Optional
import pendulum
from dataclasses import asdict

from scraper import WeatherData
from config import TEMP_THRESHOLDS

console = Console()

class WeatherDisplay:
    """Rich-based weather data display system"""

    def __init__(self):
        self.console = console

    def show_weather_summary(self, weather_data: WeatherData):
        """
        Display comprehensive weather summary

        Args:
            weather_data: Weather data to display
        """
        # Create main weather panel
        main_panel = self._create_main_weather_panel(weather_data)

        # Create details table (simplified - no UV index)
        details_table = self._create_details_table(weather_data)

        # Create hourly forecast preview
        forecast_panel = self._create_forecast_preview(weather_data)

        # Display all components
        console.print("\n")
        console.print(main_panel)
        console.print("\n")
        console.print(details_table)

        if weather_data.hourly_forecast:
            console.print("\n")
            console.print(forecast_panel)

    def _create_main_weather_panel(self, weather_data: WeatherData) -> Panel:
        """Create main weather information panel"""
        # Extract temperature value for styling (now Celsius)
        temp_value = self._extract_temperature_value(weather_data.current_temp)
        temp_style = self._get_temperature_style_celsius(temp_value)

        # Create main content
        location_text = Text(weather_data.location, style="bold cyan", justify="center")
        temp_text = Text(weather_data.current_temp, style=temp_style, justify="center")
        condition_text = Text(weather_data.condition, style="italic", justify="center")

        # Add feels like if available
        content = Text()
        content.append(location_text)
        content.append("\n\n")
        content.append(temp_text)
        content.append("\n")
        content.append(condition_text)

        # Add feels like temperature
        if weather_data.feels_like:
            content.append("\n")
            content.append(f"Feels Like: {weather_data.feels_like}", style="dim")

        # Add forecast range if available
        if weather_data.forecast_high_low:
            content.append("\n")
            content.append(f"Forecast: {weather_data.forecast_high_low}", style="dim")

        content.append("\n\n")

        # Add timestamp
        timestamp = pendulum.parse(weather_data.timestamp).format('MMMM DD, YYYY at HH:mm')
        content.append(f"Updated: {timestamp}", style="dim")

        return Panel(
            Align.center(content),
            title="🌤️ Current Weather",
            border_style="blue",
            padding=(1, 2)
        )

    def _create_details_table(self, weather_data: WeatherData) -> Table:
        """Create detailed weather information table (removed UV index and status)"""
        table = Table(title="Weather Details", show_header=True, header_style="bold magenta")
        table.add_column("Parameter", style="cyan", width=15)
        table.add_column("Value", style="green", width=30)

        # Add essential weather parameters only
        details = [
            ("🌡️ Temperature", weather_data.current_temp),
            ("🌡️ Feels Like", weather_data.feels_like or "N/A"),
            ("☁️ Condition", weather_data.condition),
            ("💧 Humidity", weather_data.humidity or "N/A"),
            ("💨 Wind", weather_data.wind or "N/A"),
            ("🌀 Pressure", weather_data.pressure or "N/A"),
            ("👀 Visibility", weather_data.visibility or "N/A"),
        ]

        for param, value in details:
            table.add_row(param, str(value))

        return table

    def _create_forecast_preview(self, weather_data: WeatherData) -> Panel:
        """Create hourly forecast preview panel"""
        if not weather_data.hourly_forecast:
            return Panel("No hourly forecast available", title="📅 Hourly Forecast")

        # Show first 12 hours
        preview_hours = weather_data.hourly_forecast[:12]

        forecast_table = Table(show_header=True, header_style="bold cyan")
        forecast_table.add_column("Time", style="white", width=8)
        forecast_table.add_column("Temp", style="yellow", width=10)
        forecast_table.add_column("Condition", style="green", width=20)

        for hour_data in preview_hours:
            time_str = hour_data.get('time', 'N/A')
            temp_str = hour_data.get('temperature', 'N/A')
            condition_str = hour_data.get('condition', 'N/A')[:18]  # Truncate long conditions

            forecast_table.add_row(time_str, temp_str, condition_str)

        return Panel(
            forecast_table,
            title="📅 Hourly Forecast Preview (Next 12 Hours)",
            border_style="green"
        )

    def show_full_hourly_forecast(self, weather_data: WeatherData):
        """Display complete hourly forecast (simplified - no temperature analysis)"""
        if not weather_data.hourly_forecast:
            console.print("❌ No hourly forecast data available.", style="red")
            return

        console.print(f"\n📅 Complete Hourly Forecast for {weather_data.location}", style="bold cyan")

        # Create comprehensive forecast table
        forecast_table = Table(show_header=True, header_style="bold magenta")
        forecast_table.add_column("Hour", style="cyan", width=8)
        forecast_table.add_column("Temperature", style="red", width=12)
        forecast_table.add_column("Condition", style="green", width=25)
        forecast_table.add_column("Trend", style="yellow", width=10)

        prev_temp = None

        for i, hour_data in enumerate(weather_data.hourly_forecast):
            time_str = hour_data.get('time', f'{i:02d}:00')
            temp_str = hour_data.get('temperature', 'N/A')
            condition_str = hour_data.get('condition', 'N/A')

            # Calculate trend
            current_temp = self._extract_temperature_value(temp_str)
            trend = ""
            if prev_temp is not None and current_temp is not None:
                if current_temp > prev_temp:
                    trend = "📈 Rising"
                elif current_temp < prev_temp:
                    trend = "📉 Falling"
                else:
                    trend = "➡️ Stable"
            prev_temp = current_temp

            forecast_table.add_row(time_str, temp_str, condition_str, trend)

        console.print(forecast_table)

        # Show basic forecast statistics (simplified)
        temperatures = [self._extract_temperature_value(hour.get('temperature', '')) 
                      for hour in weather_data.hourly_forecast]
        temperatures = [t for t in temperatures if t is not None]

        if temperatures:
            self._show_simple_forecast_stats(temperatures, weather_data.location)

    def _show_simple_forecast_stats(self, temperatures: List[float], location: str):
        """Show simplified forecast statistics"""
        import numpy as np

        stats_table = Table(title=f"📊 Basic Statistics - {location}")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        min_temp = min(temperatures)
        max_temp = max(temperatures)
        avg_temp = np.mean(temperatures)

        stats_table.add_row("Minimum", f"{min_temp:.1f}°C")
        stats_table.add_row("Maximum", f"{max_temp:.1f}°C")
        stats_table.add_row("Average", f"{avg_temp:.1f}°C")

        console.print("\n")
        console.print(stats_table)

    def show_date_range_results(self, range_data: Dict[str, Dict]):
        """
        Display date range temperature query results

        Args:
            range_data: Dictionary with dates and their temperature data
        """
        if not range_data:
            console.print("❌ No date range data to display.", style="red")
            return

        console.print("\n📅 Date Range Temperature Analysis", style="bold cyan")

        # Create date range table
        range_table = Table(show_header=True, header_style="bold magenta")
        range_table.add_column("Date", style="cyan", width=12)
        range_table.add_column("6:00 AM", style="blue", width=10)
        range_table.add_column("12:00 PM", style="yellow", width=10)
        range_table.add_column("6:00 PM", style="orange3", width=10)
        range_table.add_column("12:00 AM", style="purple", width=10)
        range_table.add_column("Daily Range", style="green", width=12)

        all_temperatures = []

        for date_str, day_data in range_data.items():
            temps = day_data.get('temperatures', {})

            temp_6am = temps.get('06:00', 'N/A')
            temp_12pm = temps.get('12:00', 'N/A')
            temp_6pm = temps.get('18:00', 'N/A')
            temp_12am = temps.get('00:00', 'N/A')

            # Calculate daily range
            temp_values = [self._extract_temperature_value(t) for t in temps.values()]
            temp_values = [t for t in temp_values if t is not None]

            if temp_values:
                daily_range = f"{min(temp_values):.1f} - {max(temp_values):.1f}°C"
                all_temperatures.extend(temp_values)
            else:
                daily_range = "N/A"

            range_table.add_row(
                date_str,
                str(temp_6am),
                str(temp_12pm),
                str(temp_6pm),
                str(temp_12am),
                daily_range
            )

        console.print(range_table)

        # Show overall statistics
        if all_temperatures:
            self._show_range_statistics(all_temperatures, len(range_data))

    def _show_range_statistics(self, temperatures: List[float], num_days: int):
        """Show statistics for date range data"""
        import numpy as np

        console.print(f"\n📊 Overall Statistics ({num_days} days)", style="bold yellow")

        stats_table = Table()
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        min_temp = min(temperatures)
        max_temp = max(temperatures)
        avg_temp = np.mean(temperatures)
        std_temp = np.std(temperatures)

        stats_table.add_row("Period Min", f"{min_temp:.1f}°C")
        stats_table.add_row("Period Max", f"{max_temp:.1f}°C")
        stats_table.add_row("Average", f"{avg_temp:.1f}°C")
        stats_table.add_row("Std Deviation", f"{std_temp:.1f}°C")
        stats_table.add_row("Total Range", f"{max_temp - min_temp:.1f}°C")

        console.print(stats_table)

    def _extract_temperature_value(self, temp_str: str) -> Optional[float]:
        """Extract numeric temperature value (now expects Celsius)"""
        import re

        if not temp_str or temp_str == 'N/A':
            return None

        match = re.search(r'(-?\d+(?:\.\d+)?)', str(temp_str))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def _get_temperature_style_celsius(self, temp_value: Optional[float]) -> str:
        """Get rich style for temperature based on Celsius value"""
        if temp_value is None:
            return "white"

        # Celsius thresholds
        if temp_value < 10:
            return "bold blue"  # Cold
        elif temp_value < 20:
            return "bold green"  # Mild
        elif temp_value < 30:
            return "bold yellow"  # Warm
        else:
            return "bold red"  # Hot

    def _get_temperature_description(self, temp_str: str) -> str:
        """Get temperature description for Celsius"""
        temp_value = self._extract_temperature_value(temp_str)
        if temp_value is None:
            return ""

        if temp_value < 0:
            return "❄️ Freezing"
        elif temp_value < 10:
            return "🧊 Cold"
        elif temp_value < 20:
            return "😊 Cool"
        elif temp_value < 30:
            return "🌞 Warm"
        elif temp_value < 35:
            return "🔥 Hot"
        else:
            return "🌡️ Very Hot"

    def _get_condition_emoji(self, condition: str) -> str:
        """Get emoji for weather condition"""
        if not condition:
            return ""

        condition_lower = condition.lower()

        if 'clear' in condition_lower or 'sunny' in condition_lower:
            return "☀️"
        elif 'cloud' in condition_lower or 'cloudy' in condition_lower:
            return "☁️"
        elif 'rain' in condition_lower:
            return "🌧️"
        elif 'snow' in condition_lower:
            return "❄️"
        elif 'storm' in condition_lower:
            return "⛈️"
        elif 'fog' in condition_lower:
            return "🌫️"
        else:
            return "🌤️"

    def _get_humidity_status(self, humidity: Optional[str]) -> str:
        """Get humidity status description"""
        if not humidity or humidity == 'N/A':
            return ""

        # Try to extract percentage
        import re
        match = re.search(r'(\d+)', humidity)
        if match:
            try:
                humidity_val = int(match.group(1))
                if humidity_val < 30:
                    return "🏜️ Dry"
                elif humidity_val < 60:
                    return "😊 Comfortable"
                elif humidity_val < 80:
                    return "💧 Humid"
                else:
                    return "💦 Very Humid"
            except ValueError:
                pass

        return ""

    def show_error(self, message: str, title: str = "Error"):
        """Display error message with styling"""
        error_panel = Panel(
            message,
            title=f"❌ {title}",
            border_style="red",
            padding=(1, 2)
        )
        console.print(error_panel)

    def show_success(self, message: str, title: str = "Success"):
        """Display success message with styling"""
        success_panel = Panel(
            message,
            title=f"✅ {title}",
            border_style="green",
            padding=(1, 2)
        )
        console.print(success_panel)

    def show_info(self, message: str, title: str = "Info"):
        """Display info message with styling"""
        info_panel = Panel(
            message,
            title=f"ℹ️ {title}",
            border_style="blue",
            padding=(1, 2)
        )
        console.print(info_panel)
