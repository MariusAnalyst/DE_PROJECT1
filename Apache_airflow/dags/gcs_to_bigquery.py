from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime
import os

# Configuration
PROJECT_ID = "teraform-mar"
DATASET_ID = "Mar_Mental_Health_Big_Data_Project"
TABLE_ID = "mental_health_data"
BUCKET_NAME = "mar_mental_health_bucket"
SOURCE_OBJECTS = "mental_health_data/*.parquet"
DATA_PATH = "/opt/airflow/data"
KEY_PATH = "/opt/airflow/key/teraform-mar-0fb97fcd6586.json"
KAGGLE_DATASET = "divaniazzahra/mental-health-dataset"

# Function to download dataset from Kaggle
def download_kaggle_dataset(dataset: str, download_path: str):
    """
    Downloads and unzips a dataset from Kaggle.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=download_path, unzip=True, force=True)
    print(f"Dataset '{dataset}' has been downloaded and unzipped to '{download_path}'.")

# Function to upload data to GCS using PySpark
def upload_to_gcs(data_path: str, key_path: str):
    """
    Reads the downloaded CSV and uploads it to GCS as Parquet using PySpark.
    """
    from pyspark.sql import SparkSession, types
    
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("MentalHealthDataUpload") \
        .config("spark.jars.packages", "com.google.cloud.bigdataoss:gcs-connector:hadoop3-2.2.5") \
        .getOrCreate()

    # Set Hadoop configurations to use the Service Account JSON key
    conf = spark._jsc.hadoopConfiguration()
    conf.set("google.cloud.auth.service.account.enable", "true")
    conf.set("google.cloud.auth.service.account.json.keyfile", key_path)
    conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")

    # Define Schema
    schema = types.StructType([
        types.StructField("Timestamp", types.TimestampType(), True),
        types.StructField("Gender", types.StringType(), True),
        types.StructField("Country", types.StringType(), True),
        types.StructField("Occupation", types.StringType(), True),
        types.StructField("self_employed", types.StringType(), True),
        types.StructField("family_history", types.StringType(), True),
        types.StructField("treatment", types.StringType(), True),
        types.StructField("Days_Indoors", types.StringType(), True),
        types.StructField("Growing_Stress", types.StringType(), True),
        types.StructField("Changes_Habits", types.StringType(), True),
        types.StructField("Mental_Health_History", types.StringType(), True),
        types.StructField("Mood_Swings", types.StringType(), True),
        types.StructField("Coping_Struggles", types.StringType(), True),
        types.StructField("Work_Interest", types.StringType(), True),
        types.StructField("Social_Weakness", types.StringType(), True),
        types.StructField("mental_health_interview", types.StringType(), True),
        types.StructField("care_options", types.StringType(), True),
    ])

    # Read CSV
    csv_file = os.path.join(data_path, 'Mental Health Dataset.csv')
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"File not found: {csv_file}")

    df = spark.read \
        .option("header", "true") \
        .schema(schema) \
        .csv(csv_file)

    # Write to GCS
    gcs_bucket_path = f"gs://{BUCKET_NAME}/mental_health_data/"
    df.write.mode("overwrite").parquet(gcs_bucket_path)
    print(f"Data successfully uploaded to {gcs_bucket_path}")
    
    spark.stop()

# BigQuery Table Schema Fields
BQ_TABLE_SCHEMA = [
    {"name": "Timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "Gender", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Country", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Occupation", "type": "STRING", "mode": "NULLABLE"},
    {"name": "self_employed", "type": "STRING", "mode": "NULLABLE"},
    {"name": "family_history", "type": "STRING", "mode": "NULLABLE"},
    {"name": "treatment", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Days_Indoors", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Growing_Stress", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Changes_Habits", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Mental_Health_History", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Mood_Swings", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Coping_Struggles", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Work_Interest", "type": "STRING", "mode": "NULLABLE"},
    {"name": "Social_Weakness", "type": "STRING", "mode": "NULLABLE"},
    {"name": "mental_health_interview", "type": "STRING", "mode": "NULLABLE"},
    {"name": "care_options", "type": "STRING", "mode": "NULLABLE"},
]

with DAG(
    dag_id="mental_health_full_pipeline",
    start_date=datetime(2026, 4, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    # 1. Download from Kaggle
    download_task = PythonOperator(
        task_id="download_from_kaggle",
        python_callable=download_kaggle_dataset,
        op_kwargs={
            "dataset": KAGGLE_DATASET,
            "download_path": DATA_PATH
        },
    )

    # 2. Upload to GCS as Parquet via PySpark
    upload_to_gcs_task = PythonOperator(
        task_id="upload_to_gcs_parquet",
        python_callable=upload_to_gcs,
        op_kwargs={
            "data_path": DATA_PATH,
            "key_path": KEY_PATH
        },
    )

    # 3. Create Partitioned BigQuery Table
    create_bq_table = BigQueryInsertJobOperator(
        task_id="create_partitioned_bq_table",
        configuration={
            "query": {
                "query": f"""
                    CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
                    (
                        Timestamp TIMESTAMP,
                        Gender STRING,
                        Country STRING,
                        Occupation STRING,
                        self_employed STRING,
                        family_history STRING,
                        treatment STRING,
                        Days_Indoors STRING,
                        Growing_Stress STRING,
                        Changes_Habits STRING,
                        Mental_Health_History STRING,
                        Mood_Swings STRING,
                        Coping_Struggles STRING,
                        Work_Interest STRING,
                        Social_Weakness STRING,
                        mental_health_interview STRING,
                        care_options STRING
                    )
                    PARTITION BY DATE(Timestamp);
                """,
                "useLegacySql": False,
            }
        },
    )

    # 4. Load from GCS to BigQuery
    load_gcs_to_bq = GCSToBigQueryOperator(
        task_id="load_gcs_parquet_to_bigquery",
        bucket=BUCKET_NAME,
        source_objects=[SOURCE_OBJECTS],
        destination_project_dataset_table=f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}",
        schema_fields=BQ_TABLE_SCHEMA,
        source_format="PARQUET",
        write_disposition="WRITE_TRUNCATE",
    )

    download_task >> upload_to_gcs_task >> create_bq_table >> load_gcs_to_bq
