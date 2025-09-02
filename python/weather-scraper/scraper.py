"""Web scraping functions for weather data."""

import os
import json
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import pendulum
from rich.console import Console
from config import *

console = Console()


def get_cities(country="india", force_refresh=False):
    """Fetch and cache cities for a given country."""
    filename = os.path.join(DATA_DIR, CITIES_FILE_TEMPLATE.format(country))
    
    if not force_refresh and os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)

    url = COUNTRY_URL_TEMPLATE.format(country)
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"❌ Network error while fetching cities: {e}", style="bold red")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    cities = []
    
    for a in soup.select(f"a[href^='/weather/{country}/']"):
        href = a.get("href", "")
        parts = href.split("/")
        if len(parts) >= 4 and parts[2] == country:
            city = parts[3].strip()
            if city and city != country:
                cities.append(city)

    cities = sorted(set(cities))
    
    with open(filename, "w") as f:
        json.dump(cities, f, indent=4)
    
    return cities


def fetch_today_weather(country, city):
    """Fetch current weather data for a city."""
    url = CITY_URL_TEMPLATE.format(country, city.lower().strip())
    
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as e:
        console.print(f"❌ Network error while fetching weather: {e}", style="bold red")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"class": "table table--left table--inner-borders-rows"})
    
    if not table:
        console.print("❌ Weather info table not found.", style="bold red")
        return None

    data = {}
    for row in table.find_all("tr"):
        header = row.find("th")
        value = row.find("td")
        if header and value:
            key = header.get_text(strip=True).replace(":", "")
            val = value.get_text(strip=True)
            data[key] = val
    
    return data


def _looks_like_no_data(df: pd.DataFrame) -> bool:
    """Check if DataFrame contains 'no data' indicators."""
    if df is None or df.empty:
        return True
    txt = df.astype(str)
    return txt.apply(lambda s: s.str.contains("No data available", case=False)).any().any()


def fetch_historic_weather(country: str, city: str, date_str: str) -> pd.DataFrame | None:
    """Fetch historic weather data for a specific date."""
    urls = [
        f"https://www.timeanddate.com/weather/{country}/{city}/historic?hd={date_str}",
        f"https://www.timeanddate.com/weather/{country}/{city}/historic?start={date_str}",
    ]
    
    for url in urls:
        console.print(f"[cyan]Fetching:[/] {url}")
        
        try:
            response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as e:
            console.print(f"❌ Network error: {e}", style="bold red")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", id="wt-his") or soup.find("table", {"class": "zebra tb-wt fw va-m tb-hover"})
        
        if not table:
            continue

        try:
            raw = pd.read_html(StringIO(str(table)))
        except ValueError:
            continue
            
        if not raw:
            continue

        df = raw[0].copy()

        if _looks_like_no_data(df):
            continue

        # Handle MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [
                "_".join([str(c) for c in col if c and str(c) != "nan"]).strip("_")
                for col in df.columns
            ]
        else:
            df.columns = [str(c) for c in df.columns]

        # Rename columns
        rename_map = {
            "Unnamed: 0_level_0_Time": "Time",
            "Time": "Time",
            "Conditions_Temp": "Temperature",
            "Conditions_Weather": "Weather",
            "Conditions_Wind": "Wind",
            "Conditions": "Weather",
            "Comfort_Humidity": "Humidity",
            "Comfort_Barometer": "Barometer",
            "Comfort_Visibility": "Visibility",
        }
        df.rename(columns=rename_map, inplace=True)

        # Fix Time column
        if "Time" not in df.columns:
            time_like = [c for c in df.columns if "Time" in c]
            if time_like:
                df.rename(columns={time_like[0]: "Time"}, inplace=True)

        # Remove ads/promotional content
        df = df[~df.apply(lambda row: row.astype(str).str.contains("CustomWeather", case=False).any(), axis=1)]

        # Extract temperature from weather column if needed
        if ("Temperature" not in df.columns) and ("Weather" in df.columns):
            df["Temperature"] = df["Weather"].str.extract(r"(-?\d+)\s*°\s*C", flags=re.IGNORECASE)[0]
            df["Weather"] = (
                df["Weather"]
                .str.replace(r"-?\d+\s*°\s*C", "", regex=True, flags=re.IGNORECASE)
                .str.strip(" .")
            )

        # Keep only wanted columns
        wanted = ["Time", "Temperature", "Weather", "Wind", "Humidity", "Barometer", "Visibility"]
        df = df[[c for c in wanted if c in df.columns]]

        # Clean and parse time
        if "Time" in df.columns:
            df["Time_clean"] = df["Time"].astype(str).str.extract(r"(\d{1,2}[:.]\d{2})")[0]
            df["Time_clean"] = df["Time_clean"].str.replace(".", ":", regex=False)
            df["Time_parsed"] = pd.to_datetime(df["Time_clean"], format="%H:%M", errors="coerce").dt.time
            df = df.dropna(subset=["Time_parsed"])
            df["Time"] = df["Time_parsed"].astype(str).str[:5]
            df = df.sort_values("Time_parsed").reset_index(drop=True)

        if not df.empty and ("Temperature" in df.columns or "Weather" in df.columns):
            return df

    console.print("❌ No historic data available for that date.", style="bold red")
    return None


def fetch_date_range_weather(country: str, city: str, start_date: str, end_date: str):
    """Fetch weather data for a date range at specific times (6am, 12pm, 6pm, 12am)."""
    start = pendulum.parse(start_date)
    end = pendulum.parse(end_date)
    
    if start > end:
        console.print("❌ Start date cannot be after end date.", style="bold red")
        return None
    
    all_data = []
    current_date = start
    
    console.print(f"[cyan]Fetching weather data from {start_date} to {end_date}...[/]")
    
    while current_date <= end:
        date_str = current_date.format("YYYYMMDD")
        console.print(f"[yellow]Processing {current_date.format('YYYY-MM-DD')}...[/]")
        
        df = fetch_historic_weather(country, city, date_str)
        if df is not None and not df.empty:
            # Filter for specific times: 6am, 12pm, 6pm, 12am
            target_times = ["06:00", "12:00", "18:00", "00:00"]
            for target_time in target_times:
                closest_row = df.iloc[(pd.to_datetime(df["Time"], format="%H:%M", errors="coerce") - 
                                     pd.to_datetime(target_time, format="%H:%M")).abs().argsort()[:1]]
                if not closest_row.empty:
                    row_data = closest_row.iloc[0].copy()
                    row_data["Date"] = current_date.format("YYYY-MM-DD")
                    row_data["Target_Time"] = target_time
                    all_data.append(row_data)
        
        current_date = current_date.add(days=1)
    
    if all_data:
        result_df = pd.DataFrame(all_data)
        # Reorder columns
        cols = ["Date", "Target_Time", "Time"] + [c for c in result_df.columns if c not in ["Date", "Target_Time", "Time"]]
        result_df = result_df[[c for c in cols if c in result_df.columns]]
        return result_df
    
    return None


def fetch_last_24hrs_weather(country: str, city: str):
    """Fetch weather data for the last 24 hours."""
    today = pendulum.now()
    yesterday = today.subtract(days=1)
    
    # Try to get data from yesterday and today
    all_data = []
    
    for date in [yesterday, today]:
        date_str = date.format("YYYYMMDD")
        df = fetch_historic_weather(country, city, date_str)
        if df is not None and not df.empty:
            df["Date"] = date.format("YYYY-MM-DD")
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by date and time
        combined_df["DateTime"] = pd.to_datetime(
            combined_df["Date"] + " " + combined_df["Time"], 
            format="%Y-%m-%d %H:%M", 
            errors="coerce"
        )
        combined_df = combined_df.dropna(subset=["DateTime"])
        combined_df = combined_df.sort_values("DateTime")
        
        # Filter last 24 hours
        now = pendulum.now()
        twenty_four_hours_ago = now.subtract(hours=24)
        
        mask = combined_df["DateTime"] >= twenty_four_hours_ago.to_datetime_string()
        return combined_df[mask].reset_index(drop=True)
    
    return None