from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}


def transform_data():
    print("Transforming mental health data...")


def load_data():
    print("Loading mental health data to BigQuery...")



with DAG(
    'sample_mental_health_pipeline',
    default_args=default_args,
    description='Sample DAG for Mental Health Data Pipeline',
    schedule='@daily',
    catchup=False,
    tags=['mental_health', 'sample'],
) as dag:

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    transform_task >> load_task