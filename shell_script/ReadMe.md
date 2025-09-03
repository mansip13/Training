# Shell Scripting & Automation Training

This repository contains practice scripts and a mini-project demonstrating key concepts in shell scripting, automation of data movement tasks, and job scheduling with cron. It also includes practical ETL and ELT pipelines, implemented with a combination of shell scripts and Python for data transformation.

## Overview

This training covers fundamental shell scripting concepts and demonstrates their application in real-world automation scenarios. The project emphasizes practical skills for system administration, data processing, and workflow automation.

## Concepts Covered

### 1. Shell Scripting Basics
- Writing reusable scripts with `#!/bin/bash`
- Using variables (`$var`), loops (`for`, `while`), and conditionals (`if`)
- Reading user input with `read`
- Command substitution (`$(command)`)
- Logging outputs with `>` (overwrite) and `>>` (append)

### 2. Automation of Data Movement
- Moving and copying files with `mv`, `cp`
- Automated backups with timestamps
- Organizing files into structured directories

### 3. Scheduling Jobs with Cron
- Automating repetitive tasks at scheduled times
- Cron syntax (`* * * * *`)
- Example cron job:
  ```cron
  0 2 * * * /home/user/scripts/etl.sh >> /home/user/logs/etl.log 2>&1
  ```

## Practice Scripts

### System Info Script
Displays comprehensive system information including:
- Hostname
- System uptime
- Memory usage statistics
- Current CPU load
- Available disk space

**Usage:**
```bash
bash practice/system_info.sh
```

### File Organizer Script
Automatically organizes files by extension into structured subdirectories:
- `.txt` files → `docs/`
- `.jpg` files → `images/`
- `.csv` files → `data/`

**Usage:**
```bash
bash practice/file_organizer.sh
```

### Calculator Script
Interactive command-line calculator supporting basic arithmetic operations:
- Addition (+)
- Subtraction (-)
- Multiplication (*)
- Division (/)

**Usage:**
```bash
bash practice/calculator.sh
```

## Mini-Project: ETL & ELT Pipelines

The project demonstrates two common data workflow patterns using shell scripts integrated with Python for data transformation tasks.

### ETL vs ELT: Understanding the Difference

**ETL (Extract-Transform-Load):**
- Data is extracted from source systems
- Transformations are applied before loading
- Clean, processed data is loaded into the target system
- Better for smaller datasets where transformation logic is complex
- Provides data validation before loading

**ELT (Extract-Load-Transform):**
- Data is extracted and immediately loaded into the target system
- Transformations are performed after loading, within the target system
- Leverages the processing power of modern data warehouses
- Better for large datasets and cloud-based architectures
- Allows for more flexible, on-demand transformations

### ETL Pipeline Implementation

**Process Flow:**
1. **Extract (Shell Script)**: Copies CSV files from `data/` to `temp/`
2. **Transform (Python Wrangler)**: Cleans and processes data:
   - Replaces blank cells with "NA"
   - Drops completely empty rows
   - Standardizes column headers (lowercase with underscores)
   - Adds sequential row_number column
3. **Load (Shell Script)**: Moves transformed CSVs to `processed/` folder

**Usage:**
```bash
bash project/scripts/etl.sh
```

### ELT Pipeline Implementation

**Process Flow:**
1. **Extract + Load (Shell Script)**: Copies CSV files from `data/` into `backups/` with timestamps
2. **Transform (Python Wrangler)**: Processes CSVs in place after loading

**Usage:**
```bash
bash project/scripts/elt.sh
```

### Python Wrangler Module

The `wrangler.py` script serves both ETL and ELT pipelines and performs:
- Removal of rows containing only NaN values
- Replacement of empty cells with "NA"
- Standardization of column headers
- Addition of sequential row numbering

**Manual Usage:**
```bash
python3 project/scripts/wrangler.py project/backups/
```

## Repository Structure

```
Training/
└── shell_scripting/
    ├── practice/
    │   ├── system_info.sh      # System information display
    │   ├── file_organizer.sh   # File organization utility
    │   └── calculator.sh       # Command-line calculator
    ├── project/
    │   ├── data/              # Raw CSV input files
    │   ├── backups/           # Timestamped backups (ELT)
    │   ├── temp/              # Temporary processing folder (ETL)
    │   ├── processed/         # Final processed output (ETL)
    │   ├── logs/              # Cron job and execution logs
    │   └── scripts/
    │       ├── etl.sh         # ETL pipeline script
    │       ├── elt.sh         # ELT pipeline script
    │       └── wrangler.py    # Python data transformation module
    └── README.md
```

## Automation with Cron

### Setting Up Scheduled Jobs

**ETL Job (Every Hour):**
```bash
crontab -e
```
Add the following line:
```cron
0 * * * * /home/mansi/Training/shell_scripting/project/scripts/etl.sh >> /home/mansi/Training/shell_scripting/project/logs/etl.log 2>&1
```

**ELT Job (Every 30 Minutes):**
```cron
30 * * * * /home/mansi/Training/shell_scripting/project/scripts/elt.sh >> /home/mansi/Training/shell_scripting/project/logs/elt.log 2>&1
```

### Cron Syntax Reference
```
* * * * *
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```
