#!/usr/bin/env python3
"""
Weather CLI Scraper - SIMPLIFIED Main Entry Point
Enforces Country/City format for better reliability
"""

import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
import sys
import os
import pendulum
import numpy as np

# Local imports
from scraper import WeatherScraper, WeatherData
from data_handler import DataHandler
from weather_display import WeatherDisplay
from chart_generator import ChartGenerator
from date_utils import DateUtils
from config import MENU_OPTIONS

console = Console()
app = typer.Typer(help="Weather CLI Scraper for timeanddate.com")

class WeatherCLI:
    """SIMPLIFIED CLI application"""

    def __init__(self):
        self.scraper = WeatherScraper()
        self.data_handler = DataHandler()
        self.display = WeatherDisplay()
        self.chart_generator = ChartGenerator()
        self.current_weather_data: Optional[WeatherData] = None

    def show_banner(self):
        """Display application banner"""
        banner = """
🌤️  Weather CLI Scraper - SIMPLIFIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Real weather data from timeanddate.com (Country/City format required)
        """

        banner_panel = Panel(
            banner.strip(),
            style="bold blue",
            padding=(1, 2)
        )
        console.print(banner_panel)

    def show_location_format_guide(self):
        """Display MANDATORY location format"""
        format_guide = """
📍 MANDATORY Format: Country/City

✅ CORRECT Examples:
   • Japan/Tokyo
   • UK/London  
   • USA/New York
   • France/Paris
   • Germany/Berlin
   • Australia/Sydney
   • Canada/Toronto
   • India/Mumbai

❌ INCORRECT Examples:
   • Tokyo (missing country)
   • Tokyo, Japan (wrong separator)
   • japan/tokyo (wrong case)

💡 Tips:
   • Use the country name as it appears on timeanddate.com
   • Use proper capitalization
   • Use forward slash (/) as separator
        """

        guide_panel = Panel(
            format_guide.strip(),
            title="⚠️ MANDATORY: Country/City Format",
            border_style="red",
            padding=(1, 2)
        )
        console.print(guide_panel)

    def show_main_menu(self) -> str:
        """Display main menu"""
        console.print("\n" + "="*60)
        console.print("📋 MAIN MENU", style="bold cyan")
        console.print("="*60)

        menu_table = Table(show_header=False, box=None)
        menu_table.add_column("Option", style="cyan", width=5)
        menu_table.add_column("Description", style="white", width=45)

        for key, description in MENU_OPTIONS.items():
            menu_table.add_row(f"[{key}]", description)

        console.print(menu_table)
        console.print("="*60)

        choice = Prompt.ask(
            "Select an option",
            choices=list(MENU_OPTIONS.keys()),
            default="1"
        )

        return choice

    def search_weather(self):
        """Search weather with MANDATORY Country/City format"""
        console.print("\n🔍 Search Weather by Location", style="bold cyan")

        # Show mandatory format guide
        self.show_location_format_guide()

        # Get location input
        location_input = Prompt.ask(
            "\n🌍 Enter location (Country/City)",
            default="Japan/Tokyo"
        ).strip()

        if not location_input:
            self.display.show_error("Please enter a location.")
            return

        # Validate format
        if '/' not in location_input:
            self.display.show_error(
                "❌ WRONG FORMAT!\n\n"
                "You entered: " + location_input + "\n"
                "Required format: Country/City\n\n"
                "Examples:\n"
                "✅ Japan/Tokyo\n"
                "✅ UK/London\n"
                "✅ USA/New York"
            )
            return

        # Fetch REAL weather data
        console.print(f"\n🌤️ Fetching weather data for {location_input}...")
        weather_data = self.scraper.get_weather_by_location(location_input)

        if not weather_data:
            self.display.show_error(
                f"Failed to retrieve weather data for '{location_input}'.\n\n"
                "Possible issues:\n"
                "• Location not found on timeanddate.com\n"
                "• Incorrect country/city name\n"
                "• Network connection problem\n\n"
                "Try these working examples:\n"
                "✅ Japan/Tokyo\n"
                "✅ UK/London\n"
                "✅ France/Paris"
            )
            return

        # Store current weather data
        self.current_weather_data = weather_data

        # Display weather information
        self.display.show_weather_summary(weather_data)

        # Show success
        self.display.show_success(
            f"Weather data retrieved for {weather_data.location}!\n"
            f"Temperature: {weather_data.current_temp}\n"
            f"Condition: {weather_data.condition}"
        )

        # Ask if user wants to save data
        if Confirm.ask("\nWould you like to save this data?"):
            self.data_handler.interactive_save(weather_data)

    def view_hourly_forecast(self):
        """View hourly forecast (simplified)"""
        if not self.current_weather_data:
            self.display.show_error("No weather data available. Please search for a location first.")
            return

        console.print("\n📅 Hourly Forecast", style="bold cyan")

        # Show hourly forecast
        self.display.show_full_hourly_forecast(self.current_weather_data)

        # Show chart if requested
        if self.current_weather_data.hourly_forecast and Confirm.ask("\nWould you like to see a temperature chart?"):
            chart = self.chart_generator.create_hourly_temperature_chart(
                self.current_weather_data,
                f"Hourly Temperature - {self.current_weather_data.location}"
            )
            console.print("\n")
            console.print(chart)

    def save_weather_data(self):
        """Save current weather data"""
        if not self.current_weather_data:
            self.display.show_error("No weather data available to save. Please search for a location first.")
            return

        console.print("\n💾 Save Weather Data", style="bold cyan")
        self.data_handler.display_saved_files()

        success = self.data_handler.interactive_save(self.current_weather_data)

        if success:
            self.display.show_success("Weather data saved successfully!")
        else:
            self.display.show_error("Failed to save weather data.")

    def filter_by_date(self):
        """Filter by date (simplified)"""
        console.print("\n📅 Filter by Date", style="bold cyan")

        if not self.current_weather_data:
            self.display.show_error("No weather data available. Please search for a location first.")
            return

        console.print("🏗️ Date filtering requires historic data implementation", style="yellow")
        console.print("For now, showing current hourly forecast", style="dim")

        if self.current_weather_data.hourly_forecast:
            self.display.show_full_hourly_forecast(self.current_weather_data)

    def date_range_query(self):
        """Date range query (simplified)"""
        console.print("\n📅 Date Range Query", style="bold cyan")

        if not self.current_weather_data:
            self.display.show_error("No weather data available. Please search for a location first.")
            return

        console.print("🏗️ Date range queries require historic data implementation", style="yellow")
        console.print("For now, showing current weather summary", style="dim")

        self.display.show_weather_summary(self.current_weather_data)

    def run_interactive_menu(self):
        """Run the main interactive menu loop"""
        self.show_banner()

        while True:
            try:
                choice = self.show_main_menu()

                if choice == '1':
                    self.search_weather()
                elif choice == '2':
                    self.view_hourly_forecast()
                elif choice == '3':
                    self.save_weather_data()
                elif choice == '4':
                    self.filter_by_date()
                elif choice == '5':
                    self.date_range_query()
                elif choice == '6':
                    console.print("\n👋 Thank you for using Weather CLI Scraper!", style="bold green")
                    break
                else:
                    self.display.show_error("Invalid option selected.")

                # Pause before showing menu again
                if choice != '6':
                    input("\nPress Enter to continue...")
                    console.clear()

            except KeyboardInterrupt:
                console.print("\n\n👋 Goodbye!", style="bold yellow")
                break
            except Exception as e:
                self.display.show_error(f"An unexpected error occurred: {str(e)}")
                if Confirm.ask("Would you like to continue?"):
                    continue
                else:
                    break

        # Cleanup
        self.scraper.close()

# Typer CLI commands
@app.command()
def interactive():
    """Run the interactive CLI menu"""
    cli = WeatherCLI()
    cli.run_interactive_menu()

@app.command()
def search(location: str):
    """Search weather for a specific location (format: Country/City)"""
    cli = WeatherCLI()
    console.print(f"🔍 Searching weather for: {location}")

    if '/' not in location:
        console.print("❌ Wrong format! Use: Country/City (e.g., Japan/Tokyo)", style="red")
        return

    weather_data = cli.scraper.get_weather_by_location(location)
    if weather_data:
        cli.display.show_weather_summary(weather_data)
    else:
        console.print("❌ Failed to retrieve weather data.", style="red")
        console.print("💡 Try: Japan/Tokyo or UK/London", style="yellow")

    cli.scraper.close()

@app.command()
def formats():
    """Show supported location input formats"""
    cli = WeatherCLI()
    cli.show_location_format_guide()

@app.command()
def version():
    """Show version information"""
    console.print("Weather CLI Scraper v3.0.0 - Simplified Edition", style="bold cyan")
    console.print("Mandatory Country/City format for reliable data! 🌡️")

def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        cli = WeatherCLI()
        cli.run_interactive_menu()
    else:
        app()

if __name__ == "__main__":
    main()
