"""Main application for Weather CLI."""

import typer
import pendulum
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

from scraper import (
    get_cities, 
    fetch_today_weather, 
    fetch_historic_weather,
    fetch_date_range_weather,
    fetch_last_24hrs_weather
)
from display import (
    display_menu,
    display_welcome,
    display_city_list,
    display_weather_table,
    display_rich_table,
    show_statistics,
    display_scatter_plot,
    display_success,
    display_error,
    display_info,
    display_loading
)
from utils import (
    select_city,
    save_data,
    generate_filename,
    validate_date_format
)
from config import DEFAULT_COUNTRY

app = typer.Typer(help="🌦️ Comprehensive Weather CLI Application")
console = Console()

# Global variables to store session data
current_country = None
current_city = None
last_data = None
last_data_type = None


def get_country_and_city():
    """Get country and city from user input."""
    global current_country, current_city
    
    if current_country and current_city:
        use_current = Confirm.ask(
            f"Use current location: {current_city.capitalize()}, {current_country.capitalize()}?",
            default=True
        )
        if use_current:
            return current_country, current_city
    
    # Get country
    current_country = Prompt.ask(
        "Enter country name",
        default=DEFAULT_COUNTRY
    ).strip().lower()
    
    # Get cities for the country
    display_loading(f"Fetching cities for {current_country}...")
    cities = get_cities(current_country)
    
    if not cities:
        display_error(f"No cities found for {current_country}")
        return None, None
    
    # Display city options
    console.print("\n[bold cyan]Select city option:[/bold cyan]")
    console.print("1. Show full city list")
    console.print("2. Enter city name directly")
    
    choice = Prompt.ask("Choose option", choices=["1", "2"], default="1")
    
    if choice == "1":
        display_city_list(cities)
    
    current_city = select_city(cities)
    display_success(f"Selected: {current_city.capitalize()}, {current_country.capitalize()}")
    
    return current_country, current_city


def handle_today_weather():
    """Handle today's weather display and saving."""
    global last_data, last_data_type
    
    country, city = get_country_and_city()
    if not country or not city:
        return
    
    display_loading("Fetching today's weather...")
    weather_data = fetch_today_weather(country, city)
    
    if not weather_data:
        display_error("Could not fetch today's weather data")
        return
    
    display_weather_table(weather_data, f"🌤️ Today's Weather - {city.capitalize()}")
    
    last_data = weather_data
    last_data_type = "today"
    
    # Ask to save data
    if Confirm.ask("💾 Save today's weather data?", default=True):
        save_weather_data(weather_data, city, "today")


def handle_historic_weather():
    """Handle historic weather for a specific date."""
    global last_data, last_data_type
    
    country, city = get_country_and_city()
    if not country or not city:
        return
    
    # Get date input
    while True:
        date_input = Prompt.ask(
            "Enter date (YYYY-MM-DD or YYYYMMDD)",
            default=pendulum.now().subtract(days=1).format("YYYY-MM-DD")
        ).strip()
        
        date_str = validate_date_format(date_input)
        if date_str:
            break
        else:
            display_error("Invalid date format. Please use YYYY-MM-DD or YYYYMMDD")
    
    display_loading(f"Fetching historic weather for {date_input}...")
    df = fetch_historic_weather(country, city, date_str)
    
    if df is None or df.empty:
        display_error("No historic weather data available for that date")
        return
    
    # Display options
    console.print("\n[bold cyan]Display Options:[/bold cyan]")
    console.print("1. Show statistics only")
    console.print("2. Show detailed data table")
    console.print("3. Show both")
    
    display_choice = Prompt.ask("Choose option", choices=["1", "2", "3"], default="3")
    
    if display_choice in ["1", "3"]:
        show_statistics(df, f"📊 Weather Statistics - {city.capitalize()} ({date_input})")
    
    if display_choice in ["2", "3"]:
        display_rich_table(df, f"🌦️ Historic Weather - {city.capitalize()} ({date_input})")
    
    last_data = df
    last_data_type = "historic"
    
    # Ask to save data
    if Confirm.ask("💾 Save historic weather data?", default=True):
        filename_base = generate_filename(city, date_input, "historic")
        save_weather_data(df, city, "historic", filename_base)


def handle_date_range_weather():
    """Handle weather data for date range at specific times."""
    global last_data, last_data_type
    
    country, city = get_country_and_city()
    if not country or not city:
        return
    
    # Get date range
    while True:
        start_date = Prompt.ask(
            "Enter start date (YYYY-MM-DD)",
            default=pendulum.now().subtract(days=7).format("YYYY-MM-DD")
        ).strip()
        
        end_date = Prompt.ask(
            "Enter end date (YYYY-MM-DD)",
            default=pendulum.now().subtract(days=1).format("YYYY-MM-DD")
        ).strip()
        
        if validate_date_format(start_date) and validate_date_format(end_date):
            break
        else:
            display_error("Invalid date format. Please use YYYY-MM-DD")
    
    display_loading(f"Fetching weather data from {start_date} to {end_date}...")
    df = fetch_date_range_weather(country, city, start_date, end_date)
    
    if df is None or df.empty:
        display_error("No weather data available for the specified date range")
        return
    
    display_rich_table(
        df, 
        f"🌦️ Weather Range - {city.capitalize()} ({start_date} to {end_date})"
    )
    show_statistics(df, f"📊 Range Statistics - {city.capitalize()}")
    
    last_data = df
    last_data_type = "range"
    
    # Ask to save data
    if Confirm.ask("💾 Save date range weather data?", default=True):
        filename_base = generate_filename(city, f"{start_date}_to_{end_date}", "range")
        save_weather_data(df, city, "range", filename_base)


def handle_24hr_plot():
    """Handle 24-hour weather plot."""
    global last_data, last_data_type
    
    country, city = get_country_and_city()
    if not country or not city:
        return
    
    display_loading("Fetching last 24 hours weather data...")
    df = fetch_last_24hrs_weather(country, city)
    
    if df is None or df.empty:
        display_error("No weather data available for the last 24 hours")
        return
    
    # Display scatter plot
    display_scatter_plot(df, f"📈 24-Hour Temperature - {city.capitalize()}")
    
    # Show additional statistics
    show_statistics(df, f"📊 24-Hour Statistics - {city.capitalize()}")
    
    last_data = df
    last_data_type = "24hr"
    
    # Ask to save data
    if Confirm.ask("💾 Save 24-hour weather data?", default=True):
        filename_base = generate_filename(city, pendulum.now().format("YYYY-MM-DD"), "24hr")
        save_weather_data(df, city, "24hr", filename_base)


def save_weather_data(data, city, data_type, filename_base=None):
    """Save weather data with user-specified format."""
    if filename_base is None:
        filename_base = generate_filename(city, pendulum.now().format("YYYY-MM-DD"), data_type)
    
    # Get format choice
    format_choice = Prompt.ask(
        "Choose format",
        choices=["json", "csv"],
        default="json"
    )
    
    # Generate filename
    filename = f"{filename_base}.{format_choice}"
    
    # Save data
    if save_data(filename, data, format_choice):
        display_success(f"Data saved successfully as {filename}")
    else:
        display_error("Failed to save data")


def handle_save_options():
    """Handle saving of last retrieved data."""
    global last_data, last_data_type
    
    if last_data is None:
        display_error("No data available to save. Please fetch some weather data first.")
        return
    
    display_info(f"Last retrieved data type: {last_data_type}")
    
    if not Confirm.ask("Save the last retrieved data?", default=True):
        return
    
    if not current_city:
        display_error("No city information available")
        return
    
    filename_base = generate_filename(
        current_city, 
        pendulum.now().format("YYYY-MM-DD"), 
        last_data_type
    )
    
    save_weather_data(last_data, current_city, last_data_type, filename_base)


def interactive_menu():
    """Interactive menu system."""
    display_welcome()
    
    while True:
        display_menu()
        
        choice = Prompt.ask(
            "Select an option",
            choices=["1", "2", "3", "4", "5", "6"],
            default="1"
        )
        
        try:
            if choice == "1":
                handle_today_weather()
            elif choice == "2":
                handle_historic_weather()
            elif choice == "3":
                handle_date_range_weather()
            elif choice == "4":
                handle_24hr_plot()
            elif choice == "5":
                handle_save_options()
            elif choice == "6":
                display_success("Thank you for using Weather CLI! 🌦️")
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        except Exception as e:
            display_error(f"An unexpected error occurred: {e}")
        
        if choice != "6":
            console.print("\n" + "="*50 + "\n")


@app.command()
def today(
    country: str = typer.Option(DEFAULT_COUNTRY, "--country", "-c", help="Country name"),
    city: str = typer.Option(None, "--city", help="City name"),
    save_format: str = typer.Option(None, "--save", help="Save format (json/csv)")
):
    """Display today's weather."""
    global current_country, current_city
    current_country = country.lower()
    
    if not city:
        cities = get_cities(current_country)
        if not cities:
            display_error(f"No cities found for {current_country}")
            return
        display_city_list(cities)
        current_city = select_city(cities)
    else:
        current_city = city.lower()
    
    weather_data = fetch_today_weather(current_country, current_city)
    if weather_data:
        display_weather_table(weather_data, f"🌤️ Today's Weather - {current_city.capitalize()}")
        
        if save_format:
            filename = generate_filename(current_city, pendulum.now().format("YYYY-MM-DD"), "today")
            save_data(f"{filename}.{save_format}", weather_data, save_format)


@app.command()
def historic(
    date: str = typer.Argument(..., help="Date in YYYY-MM-DD format"),
    country: str = typer.Option(DEFAULT_COUNTRY, "--country", "-c", help="Country name"),
    city: str = typer.Option(None, "--city", help="City name"),
    save_format: str = typer.Option(None, "--save", help="Save format (json/csv)")
):
    """Display historic weather for a specific date."""
    global current_country, current_city
    current_country = country.lower()
    
    date_str = validate_date_format(date)
    if not date_str:
        display_error("Invalid date format. Use YYYY-MM-DD")
        return
    
    if not city:
        cities = get_cities(current_country)
        if not cities:
            display_error(f"No cities found for {current_country}")
            return
        display_city_list(cities)
        current_city = select_city(cities)
    else:
        current_city = city.lower()
    
    df = fetch_historic_weather(current_country, current_city, date_str)
    if df is not None and not df.empty:
        show_statistics(df, f"📊 Weather Statistics - {current_city.capitalize()} ({date})")
        display_rich_table(df, f"🌦️ Historic Weather - {current_city.capitalize()} ({date})")
        
        if save_format:
            filename = generate_filename(current_city, date, "historic")
            save_data(f"{filename}.{save_format}", df, save_format)


@app.command()
def plot24(
    country: str = typer.Option(DEFAULT_COUNTRY, "--country", "-c", help="Country name"),
    city: str = typer.Option(None, "--city", help="City name"),
    save_format: str = typer.Option(None, "--save", help="Save format (json/csv)")
):
    """Display 24-hour temperature plot."""
    global current_country, current_city
    current_country = country.lower()
    
    if not city:
        cities = get_cities(current_country)
        if not cities:
            display_error(f"No cities found for {current_country}")
            return
        display_city_list(cities)
        current_city = select_city(cities)
    else:
        current_city = city.lower()
    
    df = fetch_last_24hrs_weather(current_country, current_city)
    if df is not None and not df.empty:
        display_scatter_plot(df, f"📈 24-Hour Temperature - {current_city.capitalize()}")
        show_statistics(df, f"📊 24-Hour Statistics - {current_city.capitalize()}")
        
        if save_format:
            filename = generate_filename(current_city, pendulum.now().format("YYYY-MM-DD"), "24hr")
            save_data(f"{filename}.{save_format}", df, save_format)


@app.command()
def interactive():
    """Run the interactive menu system."""
    interactive_menu()


@app.command()
def version():
    """Show version information."""
    console.print("[bold blue]Weather CLI v1.0.0[/bold blue]")
    console.print("A comprehensive weather data fetching and visualization tool")


if __name__ == "__main__":
    app()