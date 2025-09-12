import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount

# Ensure Airflow can import our project code
sys.path.append('/opt/airflow/api-request')
from insert_records import main  # beer pipeline entrypoint

default_args = {
    'description': 'Orchestrating PunkAPI beer data pipeline',
    'start_date': datetime(2025, 9, 9),
    'catchup': False,
}

dag = DAG(
    dag_id='punkapi-beer-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(hours=1)  # run every hour
)

with dag:
    # Task 1: Ingest raw beer data into Postgres
    task1 = PythonOperator(
        task_id='ingest_beer_data_task',
        python_callable=main
    )
    
    # Task 2: Run dbt transformations
    task2 = DockerOperator(
        task_id='transform_beer_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(
            source='/home/mansi/repos/punk-api/dbt/my_project',   # ✅ correct path
            target='/usr/app',
            type='bind'
            ),
            Mount(
                source='/home/mansi/repos/punk-api/dbt/profiles.yml', # ✅ correct path
                target='/root/.dbt/profiles.yml',
                type='bind'
            )
        ],
        network_mode='punk-api_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
    )
    
    # Set dependencies
    task1 >> task2
