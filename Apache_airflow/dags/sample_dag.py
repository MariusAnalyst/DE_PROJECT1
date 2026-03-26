from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'sample_mental_health_pipeline',
    default_args=default_args,
    description='Sample DAG for Mental Health Data Pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['mental_health', 'sample'],
)

# Sample tasks
def extract_data():
    """Simulate data extraction from a source"""
    print("Extracting mental health data from source...")
    return "Data extracted successfully"

def transform_data():
    """Simulate data transformation"""
    print("Transforming mental health data...")
    return "Data transformed successfully"

def load_data():
    """Simulate data loading to destination"""
    print("Loading mental health data to BigQuery...")
    return "Data loaded successfully"

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# Set task dependencies
extract_task >> transform_task >> load_task