# Weather CLI Scraper

A comprehensive command-line weather data scraping and visualization tool that fetches real-time and historical weather information from timeanddate.com.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [Output Examples](#output-examples)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Overview

This Weather CLI application is a sophisticated web scraping tool that extracts weather data from timeanddate.com and presents it in various formats including interactive tables, statistical summaries, and visual plots. The application supports both current weather conditions and historical weather data analysis.

## Features

### Core Functionality
- **Real-time Weather**: Fetch current weather conditions for any city
- **Historical Data**: Retrieve weather data for specific dates
- **Date Range Analysis**: Analyze weather patterns across date ranges
- **24-Hour Visualization**: Generate temperature plots for the last 24 hours
- **Multi-format Export**: Save data in JSON or CSV formats

### User Experience
- **Interactive CLI**: Rich, colorful command-line interface
- **Menu-driven Navigation**: Easy-to-use interactive menu system
- **Command-line Interface**: Direct command execution with arguments
- **Smart City Selection**: Automatic city suggestions and search
- **Data Persistence**: Automatic caching of city lists

### Data Analysis
- **Statistical Analysis**: Temperature and humidity statistics
- **Weather Pattern Recognition**: Most common weather conditions
- **Visual Plotting**: ASCII-based temperature scatter plots
- **Time-based Filtering**: Focus on specific time ranges

## Technologies Used

### Web Scraping Stack
- **Requests**: HTTP library for web requests with timeout and header management
- **BeautifulSoup4**: HTML parsing and DOM manipulation
- **lxml**: Fast XML and HTML parser

### Data Processing
- **Pandas**: Data manipulation and analysis framework
- **NumPy**: Numerical computing for statistics
- **Pendulum**: Modern date/time handling library

### CLI & Visualization
- **Typer**: Modern CLI framework with type hints
- **Rich**: Rich text and beautiful formatting in terminal
- **Plotille**: ASCII plotting library for terminal-based visualizations

### Data Storage
- **JSON**: Structured data storage and city caching
- **CSV**: Tabular data export format

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   main.py       │    │   scraper.py    │    │   display.py    │
│   (CLI & Menu)  │◄──►│   (Web Scraping)│    │   (UI & Tables) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   utils.py      │    │   config.py     │    │   Data Files    │
│   (Utilities)   │    │   (Settings)    │    │   (JSON/CSV)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Module Responsibilities

- **`main.py`**: Application entry point, CLI commands, and interactive menu system
- **`scraper.py`**: Web scraping logic, HTTP requests, and HTML parsing
- **`display.py`**: Rich terminal UI, data visualization, and table formatting
- **`utils.py`**: Helper functions, data processing, and file operations
- **`config.py`**: Application configuration, URLs, and constants

## Installation

### Prerequisites
- Python 3.13+
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd weather-scraper

# Install dependencies
pip install -r requirements.txt

# Or install individual packages
pip install requests beautifulsoup4 lxml pandas numpy pendulum typer rich plotille
```

### Project Dependencies
```txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
pandas>=2.0.0
numpy>=1.24.0
pendulum>=2.1.0
typer>=0.9.0
rich>=13.0.0
plotille>=5.0.0
```

## Usage

### Interactive Mode
```bash
python main.py interactive
```

### Direct Commands

#### Today's Weather
```bash
# Default country (India)
python main.py today --city mumbai

# Specific country
python main.py today --country usa --city "new-york"

# Save data automatically
python main.py today --city delhi --save json
```

#### Historical Weather
```bash
# Specific date
python main.py historic 2024-01-15 --city mumbai

# With country specification
python main.py historic 2024-01-15 --country uk --city london --save csv
```

#### 24-Hour Temperature Plot
```bash
python main.py plot24 --city mumbai --save json
```

### Interactive Menu Options

1. **🌤️ Display Today's Weather**: Current weather conditions
2. **📅 Display Historic Weather**: Weather for a specific date
3. **📊 Display Weather Range**: Weather data across date ranges
4. **📈 Display Last 24 Hours Plot**: Temperature visualization
5. **💾 Save Data Options**: Export previously fetched data
6. **🚪 Exit**: Close application

## Data Flow

### 1. Web Scraping Process
```
User Input → City Validation → URL Construction → HTTP Request → HTML Parsing → Data Extraction
```

### 2. Data Processing Pipeline
```
Raw HTML → BeautifulSoup Parsing → Table Extraction → Data Cleaning → Pandas DataFrame → Statistical Analysis
```

### 3. Visualization Workflow
```
Clean Data → Rich Tables → ASCII Plots → Statistical Summaries → Export Options
```

### Key Data Processing Steps

1. **City Discovery**: Scrape city lists from country pages and cache locally
2. **Weather Extraction**: Parse structured weather tables from timeanddate.com
3. **Data Normalization**: Clean and standardize temperature, humidity, and time data
4. **Time Processing**: Convert time strings to structured time objects
5. **Statistical Computation**: Calculate min, max, average, and distribution statistics
6. **Visualization**: Generate ASCII scatter plots and rich terminal tables

## Output Examples

### Today's Weather Table
```
┌─────────────────────────────────────────┐
│           🌤️ Today's Weather           │
├────────────────┬────────────────────────┤
│ Parameter      │ Value                  │
├────────────────┼────────────────────────┤
│ Temperature    │ 28°C                   │
│ Weather        │ Partly cloudy          │
│ Wind           │ 15 km/h from SW        │
│ Humidity       │ 65%                    │
└────────────────┴────────────────────────┘
```

### Statistical Summary
```
┌─────────────────────────────────────────┐
│          📊 Weather Statistics          │
├─────────────────────────────────────────┤
│ 🌡️ Temperature Statistics:             │
│    • Average: 26.3°C                   │
│    • Minimum: 22.0°C                   │
│    • Maximum: 31.0°C                   │
│    • Data Points: 24                   │
│                                         │
│ 💧 Humidity Statistics:                │
│    • Average: 68.2%                    │
│    • Minimum: 45.0%                    │
│    • Maximum: 85.0%                    │
│    • Data Points: 24                   │
└─────────────────────────────────────────┘
```

### ASCII Temperature Plot
```
┌─────────────────────────────────────────┐
│      📈 24-Hour Temperature Plot        │
├─────────────────────────────────────────┤
│    32⡀                                  │
│      ⠱⡀                                │
│    28  ⠱⡀⢀⡠⠊⡠⠊⠉⠉⠉⠑⠒⠒⠒⠑⠒⠢⠤⣀      │
│        ⠈⠉⠁    ⠊              ⠈⠉⠉⠁  │
│    24                              ⠈⠑⠤⣀│
│                                      ⠈│
│    20⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠤⠼│
│      0    6    12   18   24            │
│           Hour (0-23)                  │
└─────────────────────────────────────────┘
```

## Project Structure

```
weather-scraper/
│
├── main.py              # Main application and CLI interface
├── scraper.py           # Web scraping and data extraction
├── display.py           # Rich terminal UI and visualization
├── utils.py             # Utility functions and helpers
├── config.py            # Configuration and constants
├── pyproject.toml       # Project metadata and dependencies
├── README.md            # Project documentation
│
├── weather_data/        # Data directory (auto-created)

```

## Configuration

### Environment Variables
- `DEFAULT_COUNTRY`: Default country for city searches (default: "india")
- `DATA_DIR`: Directory for data storage (default: "weather_data")

### Customizable Settings (`config.py`)
```python
# Request settings
REQUEST_TIMEOUT = 20  # HTTP request timeout
REQUEST_HEADERS = {"User-Agent": "..."}  # Browser headers

# File settings
DATA_DIR = "weather_data"  # Data storage directory
DEFAULT_COUNTRY = "india"  # Default country selection

# URL templates
BASE_URL = "https://www.timeanddate.com/weather"
CITY_URL_TEMPLATE = "https://www.timeanddate.com/weather/{}/{}"
```

### Data Storage
- **City Cache**: `{country}_cities.json` - Cached city lists per country
- **Weather Exports**: `{city}_{date}_{type}.{format}` - Exported weather data
- **Formats**: JSON (structured) and CSV (tabular) export options

## Error Handling

The application includes comprehensive error handling for:
- **Network Issues**: Connection timeouts, HTTP errors
- **Data Parsing**: Malformed HTML, missing tables
- **Date Validation**: Invalid date formats, future dates
- **City Selection**: Non-existent cities, empty results
- **File Operations**: Write permissions, storage errors




