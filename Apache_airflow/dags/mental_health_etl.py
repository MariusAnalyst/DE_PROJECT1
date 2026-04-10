from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# Function to download dataset
def download_kaggle_dataset(dataset: str, download_path: str = "/opt/airflow/data"):
    """
    Downloads and unzips a dataset from Kaggle.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=download_path, unzip=True, force=True)
    print(f"Dataset '{dataset}' has been downloaded and unzipped to '{download_path}'.")

# Function to process/load the data
def process_mental_health_data(data_path: str = "/opt/airflow/data"):
    """
    Reads the downloaded CSV and prints basic info to verify ingestion.
    """
    import pandas as pd
    files = [f for f in os.listdir(data_path) if f.endswith('.csv')]
    if not files:
        raise FileNotFoundError(f"No CSV files found in {data_path}")
    
    for file in files:
        df = pd.read_csv(os.path.join(data_path, file))
        print(f"Successfully loaded {file}")
        print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
        print("Data Preview:")
        print(df.head())

# Define the DAG
with DAG(
    dag_id="kaggle_ingestion_dag",
    start_date=datetime(2026, 4, 10),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    download_task = PythonOperator(
        task_id="download_from_kaggle",
        python_callable=download_kaggle_dataset,
        op_kwargs={
            "dataset": "divaniazzahra/mental-health-dataset",
            "download_path": "/opt/airflow/data"
        },
    )

    process_task = PythonOperator(
        task_id="process_and_verify_data",
        python_callable=process_mental_health_data,
        op_kwargs={
            "data_path": "/opt/airflow/data"
        },
    )

    download_task >> process_task
