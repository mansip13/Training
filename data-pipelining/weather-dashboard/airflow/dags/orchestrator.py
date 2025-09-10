import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount

sys.path.append('/opt/airflow/api-request')
from insert_records import main

default_args={
    'description': 'Orchestrating data',
    'start_date': datetime(2025,9,9),
    'catchup':False,
}

dag = DAG(
    dag_id ='weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=60)
)

with dag:
    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=main
    )
    
    task2=DockerOperator(
        task_id='transformers_data_task' ,
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source='/home/mansi/repos/weather-data/dbt/my_project', target='/usr/app',type='bind'),
            Mount(source='/home/mansi/repos/weather-data/dbt/profiles.yml', target='/root/.dbt/profiles.yml', type='bind')

        ],
        network_mode='weather-data_my-network',
        docker_url='unix://var/run/docker.sock',
        auto_remove='success'
        
    )
    
    
    task1 >> task2