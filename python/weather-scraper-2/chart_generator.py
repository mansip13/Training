"""
Chart generation functionality using plotille for temperature visualization
Handles hourly forecasts, daily trends with proper hour formatting and Celsius
"""

import plotille
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import re
import pendulum

from config import CHART_HEIGHT, CHART_WIDTH
from scraper import WeatherData

console = Console()

class ChartGenerator:
    """Generate various weather charts using plotille"""

    def __init__(self, height: int = CHART_HEIGHT, width: int = CHART_WIDTH):
        self.height = height
        self.width = width

    def create_hourly_temperature_chart(self, weather_data: WeatherData, title: str = "Hourly Temperature Forecast") -> str:
        """
        Create hourly temperature chart with proper hour formatting

        Args:
            weather_data: Weather data with hourly forecast
            title: Chart title

        Returns:
            ASCII chart string with proper hour labels
        """
        if not weather_data.hourly_forecast:
            return "❌ No hourly forecast data available for charting."

        # Extract temperature data and times
        temperatures = []
        hour_labels = []
        x_values = []

        for i, hour_data in enumerate(weather_data.hourly_forecast):
            temp_value = self._extract_temperature_value(hour_data.get('temperature', ''))
            time_str = hour_data.get('time', f'{i:02d}:00')

            if temp_value is not None:
                temperatures.append(temp_value)
                hour_labels.append(time_str)
                x_values.append(i)

        if not temperatures:
            return "❌ No valid temperature data found for charting."

        # Create the chart
        try:
            # Create basic plot
            chart = plotille.plot(
                x_values, 
                temperatures,
                height=self.height,
                width=self.width,
                X_label='Hours (24-hour format)',
                Y_label='Temperature (°C)'
            )

            # Format the chart with proper hour labels
            chart_lines = chart.split('\n')

            # Create custom x-axis labels
            x_axis_labels = self._create_hour_axis_labels(hour_labels, len(x_values))

            # Replace the bottom line with our custom hour labels
            for i, line in enumerate(chart_lines):
                if '─' in line and len(line) > 50:  # This is likely the x-axis line
                    chart_lines[i+1] = x_axis_labels  # Replace the line below
                    break

            formatted_chart = '\n'.join(chart_lines)

            # Add title and statistics
            chart_with_title = f"\n{title}\n{weather_data.location}\n{'=' * 60}\n{formatted_chart}"

            # Add temperature statistics
            stats = self._calculate_temperature_stats(temperatures)
            stats_text = f"\n📊 Range: {stats['min']:.1f}°C to {stats['max']:.1f}°C | Average: {stats['avg']:.1f}°C"

            return chart_with_title + stats_text

        except Exception as e:
            return f"❌ Error creating chart: {str(e)}"

    def _create_hour_axis_labels(self, hour_labels: List[str], total_points: int) -> str:
        """Create properly formatted hour axis labels"""
        if not hour_labels:
            return ""

        # Create labels at regular intervals
        label_positions = []
        if total_points <= 12:
            # Show every hour for 12 hours or less
            step = 1
        elif total_points <= 24:
            # Show every 2 hours for 24 hours
            step = 2
        else:
            # Show every 4 hours for more than 24 hours
            step = 4

        # Create the label line
        label_line = " " * self.width
        label_chars = list(label_line)

        # Calculate positions for labels
        for i in range(0, min(len(hour_labels), total_points), step):
            if i < len(hour_labels):
                label = hour_labels[i]
                # Calculate position in the chart width
                pos = int((i / max(total_points - 1, 1)) * (self.width - len(label)))
                if pos + len(label) < self.width:
                    for j, char in enumerate(label):
                        if pos + j < len(label_chars):
                            label_chars[pos + j] = char

        return ''.join(label_chars)

    def create_daily_temperature_chart(self, daily_data: List[Dict], title: str = "Daily Temperature Trend") -> str:
        """
        Create daily temperature chart from date range data (Celsius)

        Args:
            daily_data: List of daily temperature data
            title: Chart title

        Returns:
            ASCII chart string
        """
        if not daily_data:
            return "❌ No daily data available for charting."

        # Extract average temperatures for each day
        daily_averages = []
        day_labels = []

        for i, day_data in enumerate(daily_data):
            temps = day_data.get('temperatures', {})

            # Calculate average temperature for the day
            temp_values = [self._extract_temperature_value(t) for t in temps.values()]
            temp_values = [t for t in temp_values if t is not None]

            if temp_values:
                avg_temp = sum(temp_values) / len(temp_values)
                daily_averages.append(avg_temp)
                day_labels.append(f"Day {i+1}")

        if not daily_averages:
            return "❌ No temperature data found for daily chart."

        try:
            x_values = list(range(len(daily_averages)))

            chart = plotille.plot(
                x_values, daily_averages,
                height=self.height,
                width=self.width,
                X_label='Days',
                Y_label='Average Temperature (°C)',
                lc='red'
            )

            formatted_chart = f"\n{title}\n{'=' * 60}\n{chart}"

            # Add daily breakdown
            breakdown = "\n📅 Daily Breakdown:\n"
            for i, (label, temp) in enumerate(zip(day_labels[:7], daily_averages[:7])):
                breakdown += f"{label}: {temp:.1f}°C\n"

            return formatted_chart + breakdown

        except Exception as e:
            return f"❌ Error creating daily chart: {str(e)}"

    def _extract_temperature_value(self, temp_str: str) -> Optional[float]:
        """Extract numeric temperature value from string (expects Celsius)"""
        if not temp_str:
            return None

        # Look for temperature pattern (now expecting Celsius)
        match = re.search(r'(-?\d+(?:\.\d+)?)', str(temp_str))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None

        return None

    def _calculate_temperature_stats(self, temperatures: List[float]) -> Dict[str, float]:
        """Calculate basic temperature statistics"""
        if not temperatures:
            return {'min': 0, 'max': 0, 'avg': 0}

        temps_array = np.array(temperatures)
        return {
            'min': float(np.min(temps_array)),
            'max': float(np.max(temps_array)),
            'avg': float(np.mean(temps_array))
        }

    def generate_temperature_insights(self, temperatures: List[float], location: str = "") -> str:
        """
        Generate textual insights about temperature patterns (simplified for Celsius)

        Args:
            temperatures: List of temperature values in Celsius
            location: Location name for context

        Returns:
            Formatted insights string
        """
        if not temperatures:
            return "❌ No temperature data for analysis."

        stats = self._calculate_temperature_stats(temperatures)

        # Determine temperature category (Celsius)
        avg_temp = stats['avg']
        if avg_temp < 10:
            temp_category = "❄️ Cold"
        elif avg_temp < 20:
            temp_category = "🌤️ Cool"
        elif avg_temp < 30:
            temp_category = "🌞 Warm"
        else:
            temp_category = "🔥 Hot"

        # Calculate temperature variation
        temp_range = stats['max'] - stats['min']
        if temp_range < 5:
            variation = "Low variation"
        elif temp_range < 10:
            variation = "Moderate variation"
        else:
            variation = "High variation"

        insights = f"""
🌡️ Temperature Summary {f'for {location}' if location else ''}

📊 Statistics:
   • Average: {stats['avg']:.1f}°C
   • Minimum: {stats['min']:.1f}°C
   • Maximum: {stats['max']:.1f}°C
   • Range: {temp_range:.1f}°C

🏷️ Classification: {temp_category}
📈 Variation: {variation}
🔢 Data Points: {len(temperatures)} readings
"""

        return insights.strip()
