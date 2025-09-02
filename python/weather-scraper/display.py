"""Display functions for the Weather CLI app."""

import pandas as pd
import numpy as np
import plotille
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from utils import extract_numeric_temperature, extract_numeric_humidity, calculate_statistics

console = Console()


def display_weather_table(data, title="🌤️ Today's Weather"):
    """Display weather data in a rich table format."""
    if not data:
        console.print("[bold red]❌ No weather data available.[/]")
        return

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")

    for k, v in data.items():
        if "temperature" in k.lower():
            table.add_row(k, f"[red]{v}[/red]")
        elif "humidity" in k.lower():
            table.add_row(k, f"[blue]{v}[/blue]")
        elif "wind" in k.lower():
            table.add_row(k, f"[yellow]{v}[/yellow]")
        else:
            table.add_row(k, v)

    console.print(table)


def display_rich_table(df: pd.DataFrame, title="🌦️ Weather Data"):
    """Display DataFrame in a rich table format."""
    if df is None or df.empty:
        console.print("[bold red]❌ No rows to display.[/]")
        return

    table = Table(title=title, show_lines=True)
    
    # Get columns to display
    cols = []
    for c in ["Date", "Target_Time", "Time", "Temperature", "Weather", "Wind", "Humidity", "Barometer", "Visibility"]:
        if c in df.columns:
            cols.append(c)
    
    # Add columns to table
    for c in cols:
        if c == "Temperature":
            table.add_column(c, justify="center", style="red", no_wrap=True)
        elif c == "Humidity":
            table.add_column(c, justify="center", style="blue", no_wrap=True)
        elif c == "Time" or c == "Target_Time":
            table.add_column(c, justify="center", style="green", no_wrap=True)
        elif c == "Date":
            table.add_column(c, justify="center", style="magenta", no_wrap=True)
        else:
            table.add_column(c, justify="center", style="cyan", no_wrap=True)

    # Add rows
    for _, row in df.iterrows():
        values = []
        for c in cols:
            value = str(row.get(c, ""))
            # Truncate long values
            if len(value) > 20:
                value = value[:17] + "..."
            values.append(value)
        table.add_row(*values)

    console.print(table)


def show_statistics(df: pd.DataFrame, title="📊 Weather Statistics"):
    """Display weather statistics in a panel."""
    if df is None or df.empty:
        console.print("[bold red]❌ No data available for statistics.[/]")
        return

    stats = calculate_statistics(df)
    lines = []

    if "temperature" in stats:
        temp_stats = stats["temperature"]
        lines += [
            f"🌡️ Temperature Statistics:",
            f"   • Average: {temp_stats['avg']:.1f}°C",
            f"   • Minimum: {temp_stats['min']:.1f}°C",
            f"   • Maximum: {temp_stats['max']:.1f}°C",
            f"   • Data Points: {temp_stats['count']}",
            ""
        ]

    if "humidity" in stats:
        hum_stats = stats["humidity"]
        lines += [
            f"💧 Humidity Statistics:",
            f"   • Average: {hum_stats['avg']:.1f}%",
            f"   • Minimum: {hum_stats['min']:.1f}%",
            f"   • Maximum: {hum_stats['max']:.1f}%",
            f"   • Data Points: {hum_stats['count']}",
            ""
        ]

    if "weather" in stats:
        weather_stats = stats["weather"]
        lines += [
            f"☁️ Weather Conditions:",
            f"   • Most Common: {weather_stats['most_common']}",
        ]
        
        if weather_stats['conditions']:
            lines.append("   • All Conditions:")
            for condition, count in list(weather_stats['conditions'].items())[:5]:
                lines.append(f"     - {condition}: {count} times")

    panel_text = "\n".join([ln for ln in lines if ln])
    if not panel_text:
        panel_text = "No statistical data available."
    
    console.print(Panel(panel_text, title=title, expand=False, border_style="bright_blue"))


def display_scatter_plot(df: pd.DataFrame, title="📈 24-Hour Temperature Plot"):
    """Display a scatter plot of temperature over 24 hours using plotille."""
    if df is None or df.empty:
        console.print("[bold red]❌ No data available for plotting.[/]")
        return

    # Extract temperature and time data
    temps = df["Temperature"].apply(extract_numeric_temperature).dropna()
    if temps.empty:
        console.print("[bold red]❌ No temperature data available for plotting.[/]")
        return

    # Extract hour from time
    hours = []
    for idx in temps.index:
        if "Time" in df.columns:
            time_str = str(df.loc[idx, "Time"])
            try:
                hour = int(time_str.split(":")[0])
                hours.append(hour)
            except:
                hours.append(0)
        else:
            hours.append(0)

    if not hours:
        console.print("[bold red]❌ No time data available for plotting.[/]")
        return

    # Create the plot
    try:
        # Convert to int arrays
        x_data = np.array(hours, dtype=int)
        y_data = np.array(temps.values, dtype=int)
        
        # Create scatter plot
        plot = plotille.scatter(
            x_data, y_data,
            width=80, height=20,
            X_label="Hour (0-23)",
            Y_label="Temperature (°C)"
        )
        
        console.print(Panel(plot, title=title, border_style="green"))
        
        # Show analysis
        analysis_lines = [
            f"📊 Temperature Analysis (24 Hours):",
            f"   • Minimum Temperature: {int(y_data.min())}°C at {x_data[np.argmin(y_data)]:02d}:00",
            f"   • Maximum Temperature: {int(y_data.max())}°C at {x_data[np.argmax(y_data)]:02d}:00",
            f"   • Average Temperature: {int(y_data.mean())}°C",
            f"   • Temperature Range: {int(y_data.max() - y_data.min())}°C",
            f"   • Data Points: {len(y_data)}"
        ]
        
        analysis_text = "\n".join(analysis_lines)
        console.print(Panel(analysis_text, title="📈 Analysis", border_style="yellow"))
        
    except Exception as e:
        console.print(f"❌ Error creating plot: {e}", style="bold red")


def display_menu():
    """Display the main menu."""
    menu_text = """
🌦️ [bold blue]Weather CLI - Main Menu[/bold blue] 🌦️

[bold cyan]1.[/bold cyan] 🌤️  Display Today's Weather
[bold cyan]2.[/bold cyan] 📅  Display Historic Weather (Specific Date)
[bold cyan]3.[/bold cyan] 📊  Display Weather Range (6AM, 12PM, 6PM, 12AM)
[bold cyan]4.[/bold cyan] 📈  Display Last 24 Hours Plot
[bold cyan]5.[/bold cyan] 💾  Save Data Options
[bold cyan]6.[/bold cyan] 🚪  Exit

"""
    console.print(Panel(menu_text, border_style="bright_blue"))


def display_city_list(cities, title="Available Cities"):
    """Display list of cities in columns."""
    if not cities:
        console.print("[bold red]❌ No cities available.[/]")
        return

    console.print(f"\n[bold cyan]{title}:[/bold cyan]")
    
    # Display in columns
    cols = 3
    for i in range(0, len(cities), cols):
        row_cities = cities[i:i+cols]
        row_text = ""
        for j, city in enumerate(row_cities):
            city_num = i + j + 1
            row_text += f"{city_num:3d}. {city.capitalize():<25}"
        console.print(row_text)


def display_welcome():
    """Display welcome message."""
    welcome_text = """
[bold blue]🌦️ Weather CLI Application 🌦️[/bold blue]

Welcome to the comprehensive weather data tool!
Fetch current weather, historic data, and visualize trends.

[italic]Powered by timeanddate.com data[/italic]
"""
    console.print(Panel(welcome_text, border_style="bright_green", padding=(1, 2)))


def display_loading(message="Loading..."):
    """Display loading message."""
    console.print(f"[yellow]⏳ {message}[/yellow]")


def display_success(message):
    """Display success message."""
    console.print(f"[bold green]✅ {message}[/bold green]")


def display_error(message):
    """Display error message."""
    console.print(f"[bold red]❌ {message}[/bold red]")


def display_info(message):
    """Display info message."""
    console.print(f"[cyan]ℹ️  {message}[/cyan]")