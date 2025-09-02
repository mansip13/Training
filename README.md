# Python Learning Path - Data Manipulation, Automation & CLI Applications

A comprehensive learning journey focused on building practical Python skills for data manipulation, web scraping, and command-line application development.

## Learning Objectives

Enhance proficiency in Python for:
- **Data manipulation and analysis** using modern libraries
- **Automation and scripting** for repetitive tasks
- **CLI application development** with professional interfaces
- **Web scraping** for data collection and monitoring
- **File operations** with various data formats

## Curriculum Overview

### 1. Data Manipulation with Pandas and NumPy 
**Focus**: Core data processing and statistical analysis capabilities

**Key Concepts Covered:**
- DataFrame creation, manipulation, and analysis
- Data cleaning and transformation techniques
- Statistical computations and aggregations
- Handling missing data and duplicates
- Time series data processing

**Practical Applications:**
```python
# Data filtering and statistical analysis
df = pd.DataFrame(weather_data).drop_duplicates(subset=["Link"])
stats = {
    "avg_temp": df['temperature'].mean(),
    "min_temp": df['temperature'].min(),
    "max_temp": df['temperature'].max()
}
```

### 2. DateTime Handling with Pendulum
**Focus**: Modern date/time manipulation and formatting

**Key Concepts Covered:**
- Creating and parsing datetime objects
- Timezone handling and conversions
- Date arithmetic and comparisons
- Custom formatting for different output needs

**Practical Applications:**
```python
# Consistent timestamp generation across applications
timestamp = pendulum.now().format('DD-MM-YYYY HH:mm:ss')
```

### 3. File Operations with JSON and CSV
**Focus**: Data persistence and interchange formats

**Key Concepts Covered:**
- Reading and writing JSON files
- CSV processing with proper encoding
- Error handling for file operations
- Data format conversions

**Practical Applications:**
```python
# Multi-format data export capabilities
df.to_csv("weather_data.csv", index=False, encoding="utf-8")
df.to_json("weather_data.json", orient="records", indent=4)

# Dynamic task management with JSON persistence
def save_task(tasks):
    with open(task_file, "w") as file:
        json.dump(tasks, file, indent=4)
```

### 4. CLI Applications with Typer 
**Focus**: Professional command-line interface development

**Key Concepts Covered:**
- Command definition and argument parsing
- Interactive menu systems
- Rich terminal formatting and styling
- User input validation and confirmation
- Modular CLI architecture

**Practical Applications:**
```python
# Rich, interactive CLI interfaces
app = typer.Typer()

@app.command()
def today(city: str, country: str = "india", save: str = None):
    """Fetch today's weather for a specific city."""
    # Implementation with rich formatting
```

### 5. Web Scraping with BeautifulSoup 
**Focus**: Data extraction from web sources

**Key Concepts Covered:**
- HTML parsing and DOM navigation
- HTTP request handling with proper headers
- Data extraction from structured content
- Error handling for network operations
- Respectful scraping practices

**Practical Applications:**
```python
# Comprehensive web data extraction
soup = BeautifulSoup(response.content, "html.parser")

# Extract structured data from tables and links
for a_tag in soup.find_all("a", href=True):
    if "/news/" in link:
        news_data.append({
            "title": text,
            "link": link,
            "timestamp": pendulum.now()
        })
```

## Capstone Project: Weather CLI Scraper 

### Project Overview
A sophisticated command-line weather application demonstrating integration of all learned concepts.

### Features Implemented
- **Multi-source Data Collection**: Real-time and historical weather data
- **Interactive CLI Interface**: Menu-driven and direct command execution
- **Data Analysis Capabilities**: Statistical summaries and visualizations
- **Flexible Export Options**: JSON and CSV format support
- **Smart City Management**: Automatic city discovery and caching
- **Rich Terminal UI**: Colorful tables and ASCII plots


## Supporting Projects

News Scraper Application
Purpose: Automated news headline collection and monitoring system
Core Functionalities:

Extracts news headlines and article links from BBC News website
Implements duplicate detection and data cleaning processes
Generates timestamped entries for tracking scraping activities
Exports collected data in both CSV and JSON formats for different use cases
Demonstrates foundational web scraping principles and data structure handling

Skills Demonstrated: BeautifulSoup parsing, HTTP request handling, data deduplication, multi-format export
Task Management CLI
Purpose: Personal productivity tool with rich terminal interface
Core Functionalities:

Interactive menu-driven task management system
Add, delete, view, and update task status operations
Persistent JSON-based data storage with automatic key management
Rich table formatting with separate views for pending and completed tasks
User-friendly prompts with input validation and confirmation dialogs
Dynamic task renumbering and organized display layouts

Skills Demonstrated: Typer CLI framework, Rich terminal formatting, JSON persistence, interactive user interfaces

## Technology Stack 

### Core Libraries
- **Pandas**: Advanced data manipulation and analysis
- **NumPy**: Numerical computing and statistical operations
- **BeautifulSoup4**: HTML parsing and web scraping
- **Requests**: HTTP client with timeout and header management

### CLI & User Experience
- **Typer**: Modern CLI framework with type hints
- **Rich**: Terminal formatting, tables, and interactive elements
- **Plotille**: ASCII-based plotting for terminal visualization

### Data & Time Handling
- **Pendulum**: Modern date/time manipulation
- **JSON**: Structured data storage and configuration
- **CSV**: Tabular data export and interchange
