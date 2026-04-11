from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

# Function to download dataset from Kaggle
def download_kaggle_dataset(dataset: str, download_path: str = "/opt/airflow/data"):
    """
    Downloads and unzips a dataset from Kaggle.
    """
    from kaggle.api.kaggle_api_extended import KaggleApi
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=download_path, unzip=True, force=True)
    print(f"Dataset '{dataset}' has been downloaded and unzipped to '{download_path}'.")

# Function to upload data to GCP using PySpark
def upload_to_gcs(data_path: str = "/opt/airflow/data", key_path: str = "/opt/airflow/key/teraform-mar-0fb97fcd6586.json"):
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
    gcs_bucket_path = "gs://mar_mental_health_bucket/mental_health_data/"
    df.write.mode("overwrite").parquet(gcs_bucket_path)
    print(f"Data successfully uploaded to {gcs_bucket_path}")
    
    spark.stop()

# Define the DAG
with DAG(
    dag_id="gcp_upload",
    start_date=datetime(2026, 4, 11),
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

    upload_task = PythonOperator(
        task_id="upload_to_gcs",
        python_callable=upload_to_gcs,
        op_kwargs={
            "data_path": "/opt/airflow/data",
            "key_path": "/opt/airflow/key/teraform-mar-0fb97fcd6586.json"
        },
    )

    download_task >> upload_task
