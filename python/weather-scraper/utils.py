"""Utility functions for the Weather CLI app."""

import json
import pandas as pd
import numpy as np
import pendulum
import re
from rich.console import Console
from config import DATA_DIR
import os

console = Console()


def search_cities(cities, query):
    """Search for cities matching the query."""
    query = query.lower()
    return [c for c in cities if query in c.lower()]


def select_city(cities):
    """Interactive city selection."""
    while True:
        from rich.prompt import Prompt
        selection = Prompt.ask("\nEnter city name or number from the list").strip()
        
        if selection.isdigit():
            index = int(selection)
            if 1 <= index <= len(cities):
                return cities[index - 1]
            else:
                console.print("❌ Invalid number selection.", style="bold red")
        else:
            matches = search_cities(cities, selection)
            if not matches:
                console.print("❌ No matching cities found. Try again.", style="bold red")
            elif len(matches) == 1:
                return matches[0]
            else:
                console.print("\nMatching Cities:")
                for i, c in enumerate(matches, 1):
                    console.print(f"{i}. {c.capitalize()}")
                cities = matches


def filter_by_time_range(df: pd.DataFrame, start_hm: str, end_hm: str) -> pd.DataFrame:
    """Filter DataFrame by time range."""
    if "Time_parsed" not in df.columns:
        return df.iloc[0:0]
    
    try:
        start_t = pendulum.parse(start_hm, strict=False).time()
        end_t = pendulum.parse(end_hm, strict=False).time()
    except Exception:
        console.print("❌ Invalid time format. Use HH:MM (24h).", style="bold red")
        return df.iloc[0:0]

    tp = df["Time_parsed"]
    if tp.isna().all():
        return df.iloc[0:0]
    
    if start_t <= end_t:
        mask = (tp >= start_t) & (tp <= end_t)
    else:
        mask = (tp >= start_t) | (tp <= end_t)
    
    return df[mask]


def extract_numeric_temperature(temp_str):
    """Extract numeric temperature from string."""
    if pd.isna(temp_str):
        return np.nan
    
    match = re.search(r"(-?\d+)", str(temp_str))
    if match:
        return int(match.group(1))
    return np.nan


def extract_numeric_humidity(humidity_str):
    """Extract numeric humidity from string."""
    if pd.isna(humidity_str):
        return np.nan
    
    match = re.search(r"(\d+)", str(humidity_str))
    if match:
        return int(match.group(1))
    return np.nan


def save_data(filename, data, file_format="json"):
    """Save data to file in specified format."""
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        if file_format == "csv":
            if isinstance(data, dict):
                pd.DataFrame([data]).to_csv(filepath, index=False)
            else:
                data.to_csv(filepath, index=False)
        else:
            if isinstance(data, dict):
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
            else:
                data.to_json(filepath, orient="records", force_ascii=False, indent=4)

        console.print(f"✅ Saved as [bold green]{filepath}[/bold green]")
        return True
    except Exception as e:
        console.print(f"❌ Error saving file: {e}", style="bold red")
        return False


def generate_filename(city, date_str=None, suffix=""):
    """Generate filename based on city and date."""
    if date_str is None:
        date_str = pendulum.now().format("YYYY-MM-DD")
    
    clean_city = city.lower().replace(" ", "_")
    if suffix:
        return f"{clean_city}_{date_str}_{suffix}"
    else:
        return f"{clean_city}_{date_str}"


def validate_date_format(date_str):
    """Validate date format (YYYY-MM-DD or YYYYMMDD)."""
    try:
        if len(date_str) == 8 and date_str.isdigit():
            # YYYYMMDD format
            parsed = pendulum.parse(date_str, strict=False)
            return parsed.format("YYYYMMDD")
        elif len(date_str) == 10 and "-" in date_str:
            # YYYY-MM-DD format
            parsed = pendulum.parse(date_str, strict=False)
            return parsed.format("YYYYMMDD")
        else:
            return None
    except Exception:
        return None


def calculate_statistics(df: pd.DataFrame):
    """Calculate weather statistics from DataFrame."""
    stats = {}
    
    if "Temperature" in df.columns:
        temps = df["Temperature"].apply(extract_numeric_temperature).dropna()
        if not temps.empty:
            stats["temperature"] = {
                "avg": float(temps.mean()),
                "min": float(temps.min()),
                "max": float(temps.max()),
                "count": len(temps)
            }
    
    if "Humidity" in df.columns:
        humidity = df["Humidity"].apply(extract_numeric_humidity).dropna()
        if not humidity.empty:
            stats["humidity"] = {
                "avg": float(humidity.mean()),
                "min": float(humidity.min()),
                "max": float(humidity.max()),
                "count": len(humidity)
            }
    
    if "Weather" in df.columns:
        weather_modes = df["Weather"].dropna()
        if not weather_modes.empty:
            stats["weather"] = {
                "most_common": weather_modes.mode().iloc[0] if not weather_modes.mode().empty else "N/A",
                "conditions": weather_modes.value_counts().to_dict()
            }
    
    return stats