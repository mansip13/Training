# 🍺 PunkAPI Data Pipeline & Analytics

This project builds a modern data pipeline for [PunkAPI](https://punkapi.online/v3/), a digital archive of BrewDog beers.  
It ingests raw beer data into Postgres, transforms it with dbt, and visualizes insights in Superset.

---

## 📂 Project Structure

punk-api/
├── airflow/ # Orchestration DAGs
│ └── orchestrator.py
├── api-request/ # API ingestion
│ ├── api_request.py
│ └── insert_records.py
├── dbt/ # dbt project
│ ├── my_project/
│ │ ├── dbt_project.yml
│ │ ├── models/
│ │ │ ├── staging/
│ │ │ │ └── staging.sql
│ │ │ ├── marts/
│ │ │ │ ├── master_beer_table.sql
│ │ │ │ ├── beer_malts.sql
│ │ │ │ ├── beer_hops.sql
│ │ │ │ ├── beer_food_pairings.sql
│ │ │ │ └── reports/
│ │ │ │ ├── agg_beer_metrics.sql
│ │ │ │ ├── beer_by_year.sql
│ │ │ │ └── beer_by_contributor.sql
│ │ └── sources.yml
│ └── profiles.yml
├── docker-compose.yml
└── README.md


---

## ⚙️ Pipeline Overview

1. **Ingestion (Python + Airflow)**
   - `api_request.py`: Fetches beer data from PunkAPI.
   - `insert_records.py`: Inserts raw beer data into Postgres (`dev.raw_beer_data`).

2. **Orchestration (Airflow)**
   - `orchestrator.py` defines a DAG:
     - Task 1: Ingest data into Postgres
     - Task 2: Run dbt transformations inside a Dockerized dbt container

3. **Transformations (dbt)**
   - **Staging Layer**: `staging.sql` cleans raw data
   - **Marts Layer**:
     - `master_beer_table`: Core beer attributes
     - `beer_malts`, `beer_hops`, `beer_food_pairings`: Normalized nested arrays
   - **Reports**:
     - `agg_beer_metrics`: Global KPIs (avg ABV, IBU, etc.)
     - `beer_by_year`: Trends over time
     - `beer_by_contributor`: Contributor analysis

4. **Visualization (Superset)**
   - Connect Superset to Postgres
   - Dashboard includes:
     - KPIs (avg ABV, avg IBU, total beers, oldest/newest brew)
     - Beer catalog table
     - Time trends (beers per year, avg ABV/IBU per year)
     - Distributions (ABV, IBU, EBC)
     - Contributor analysis
     - Featured beer of the day

---

## 🛠️ Tech Stack

- **Data Source**: [PunkAPI](https://punkapi.online/v3/)
- **Database**: PostgreSQL (Dockerized)
- **Orchestration**: Apache Airflow
- **Transformations**: dbt (dbt-postgres)
- **Visualization**: Apache Superset
- **Containerization**: Docker & docker-compose

---

## 🚀 Getting Started

### 1. Clone Repo
```bash
git clone https://github.com/<your-username>/punk-api.git
cd punk-api
```

2. Start Services
 ```bash
docker compose up -d
````
4. Run Airflow DAG

- Go to http://localhost:8000
- Trigger DAG punkapi-beer-dbt-orchestrator

4. Run dbt Manually (optional)
```bash
docker compose run --rm dbt run
docker compose run --rm dbt test
```

6. Access Superset

- Go to http://localhost:8088
- Connect to Postgres database db
- Explore tables under schema dev

📊 Example Dashboard (Superset)

- **Top KPIs:** Total beers, Avg ABV, Avg IBU, Avg EBC
- **Beer Catalog:** searchable list of beers
- **Trends:** Beers brewed per year, ABV/IBU trends
- **Distributions: **Histograms for ABV, IBU, EBC
- **Contributors:** Top contributors & their beers

📌 Future Improvements

- Add incremental loads (instead of full refresh)
- Normalize mash_temp and fermentation into dedicated tables
- Create Superset filters for style/category
- Deploy Airflow + dbt to cloud (AWS/GCP)


