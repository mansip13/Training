# Training

## Overview

This training program provides hands-on experience with complementary technology stacks that form the foundation of modern automation and data processing workflows. Each module builds practical skills through real-world projects and comprehensive exercises.

---

## Training Modules

### Module 1: Python Development - Data Manipulation, Automation & CLI Applications

**Focus**: Building professional Python applications for data processing, web scraping, and command-line interfaces

**Key Learning Areas:**
- **Data Manipulation**: Advanced DataFrame operations with Pandas and NumPy
- **CLI Development**: Professional command-line applications using Typer and Rich
- **Web Scraping**: Automated data collection with BeautifulSoup and Requests
- **Date/Time Handling**: Modern datetime operations with Pendulum
- **File Operations**: Multi-format data processing (JSON, CSV, structured data)

**Core Technologies:**
- Pandas, NumPy for data analysis
- BeautifulSoup4, Requests for web scraping  
- Typer, Rich for CLI development
- Pendulum for datetime handling
- Plotille for terminal visualization

**Capstone Project**: Weather CLI Scraper - A comprehensive weather application demonstrating real-time data collection, interactive CLI interfaces, statistical analysis, and multi-format data export.

**Supporting Projects**:
- **News Scraper**: Automated headline collection with duplicate detection
- **Task Manager CLI**: Interactive productivity tool with rich terminal formatting

---

### Module 2: Shell Scripting & Automation - System Administration & Data Pipelines

**Focus**: System administration, workflow automation, and data processing pipeline development

**Key Learning Areas:**
- **Shell Scripting Fundamentals**: Variables, loops, conditionals, and command substitution
- **System Automation**: File operations, backup strategies, and system monitoring
- **Task Scheduling**: Cron job configuration and automated workflow management
- **Data Pipeline Architecture**: ETL vs ELT implementation patterns
- **Python Integration**: Combining shell scripts with Python for comprehensive solutions

**Core Technologies:**
- Bash scripting and system utilities
- Cron for job scheduling
- Python integration for data transformation
- File system operations and process management

**Pipeline Projects**:
- **ETL Pipeline**: Extract-Transform-Load workflow with data validation
- **ELT Pipeline**: Extract-Load-Transform for scalable data processing
- **System Utilities**: Information display, file organization, and calculation tools

**Key Distinction - ETL vs ELT**:
- **ETL**: Transform data before loading (better for smaller datasets, data validation)
- **ELT**: Load data first, then transform (better for large datasets, leverages target system power)

---
### Module 3: SQL - Advanced Querying & Database Design

**Focus**: Developing strong foundations in relational database management and advanced SQL querying techniques.

**Key Learning Areas:**
- **Joins**: Learn how to combine data across multiple tables using INNER, LEFT, RIGHT, and FULL joins to answer complex business questions.
- **Subqueries & CTEs**: Write reusable, modular queries and simplify complex logic with Common Table Expressions.
- **Schema Design**: Understand how to create robust tables with constraints (PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK) to ensure data integrity.
- **Date & String Functions**: Apply transformations, aggregations, and formatting functions to extract meaningful insights from raw data.
- **Indexing Basics**: Explore how indexes improve query performance and when to use them effectively.

**Core Technologies:**
- PostgreSQL (or MySQL) for relational database management
- SQL client tools (psql, DBeaver, or DB Browser)

**Capstone Project**: Library System Database – Design and implement a complete schema for managing books, authors, users, and loans. Write SQL queries to fetch overdue books, identify popular authors, and generate user borrowing histories.

**Supporting Exercises**:
- Advanced query practice on platforms like *LeetCode SQL*  
- Case studies from *SQL for Data Analysis*

---

### Module 4: Data Pipelines - Design & Orchestration

**Focus**: Building automated workflows that move, transform, and manage data at scale.

**Key Learning Areas:**
- **Pipeline Fundamentals**: Understand the difference between ETL (Extract-Transform-Load) and ELT (Extract-Load-Transform), and when to use each pattern.
- **Workflow Orchestration**: Learn how to schedule, monitor, and manage tasks with tools like Apache Airflow or Dagster.
- **ETL in Python**: Write custom Python functions for data ingestion (APIs, files), transformation (cleaning, enrichment), and loading into databases or warehouses.
- **Error Handling & Logging**: Implement strategies to ensure reliability, retries, and observability in pipelines.
- **Scalability Principles**: Explore modular pipeline design, task parallelization, and dependency management.

**Core Technologies:**
- Apache Airflow for workflow scheduling and monitoring
- Dagster for modern pipeline design
- Python for data transformation logic
- PostgreSQL (or other warehouses) as a storage destination

**Capstone Project**: API-to-Database Pipeline – Build a pipeline that ingests data from an external API, stores raw data in PostgreSQL, transforms it with dbt, and orchestrates the workflow with Airflow. Extend with dashboards in Superset for reporting.

**Supporting Projects**:
- **Mini ETL Pipeline**: Extract CSV data, transform with Python, and load into Postgres.
- **ELT Workflow**: Bulk-load JSON data into Postgres, then clean and transform it with SQL/dbt.

ools (Airflow/Dagster)
- Develop end-to-end projects combining ingestion, transformation, and visualization
