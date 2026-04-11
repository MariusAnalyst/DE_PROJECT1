# Mental Health Data Pipeline Project

## Table of Contents
- [Objective](#objective)
- [Technologies Used](#technologies-used)
- [Problem Description](#problem-description)
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
  - [GCP Project Configuration](#gcp-project-configuration)
  - [Terraform Deployment](#terraform-deployment)
  - [Docker Installation](#docker-installation)
  - [Spark Environment Setup](#spark-environment-setup)
  - [dbt Core Setup and BigQuery Configuration](#dbt-core-setup-and-bigquery-configuration)
- [dbt Implementation Details](#dbt-implementation-details)
  - [dbt Project Structure and Models](#dbt-project-structure-and-models)
  - [Running dbt Models](#running-dbt-models)
  - [Accessing Transformed Data](#accessing-transformed-data-in-bigquery)
  - [Automating dbt Jobs](#automating-dbt-jobs-to-run-daily)
  - [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
- [Next Steps](#next-steps)

## Objective
**Unlocking Insights into Mental Health: Building a Robust Data Pipeline for Global Analysis**

The primary objective of this project is to engineer an automated, end-to-end data intelligence pipeline that monitors and analyzes the global intersection of professional environments and mental health outcomes. By leveraging Airflow, PySpark, and Google Cloud Platform, the project transforms static global survey data into a dynamic analytical ecosystem. This system is designed to identify shifting trends in workplace stress, bridge the 'treatment gap' through predictive data modeling, and provide public health stakeholders with a real-time diagnostic tool to optimize workplace wellness and intervention strategies

## Technologies Used
This project leverages cutting-edge cloud and data engineering tools:

- ![Terraform](https://www.terraform.io/img/terraform-logo.png) [Terraform](https://www.terraform.io/docs) - Infrastructure as Code
- ![GCP](https://icons8.com/icons/set/google-cloud) [Google Cloud Platform (GCP)](https://cloud.google.com/docs) - Cloud Services
- ![Airflow](https://airflow.apache.org/docs/apache-airflow/stable/_images/pin_large.png) [Apache Airflow](https://airflow.apache.org/docs/) - Workflow Orchestration
- ![BigQuery](https://cloud.google.com/images/products/bigquery.png) [Google BigQuery](https://cloud.google.com/bigquery/docs) - Data Warehouse
- ![dbt](https://docs.getdbt.com/img/dbt-logo.png) [dbt](https://docs.getdbt.com/) - Data Transformation
- ![Power BI](https://powerbi.microsoft.com/pictures/application-logos/svg/powerbi.svg) [Power BI](https://docs.microsoft.com/en-us/power-bi/) - Data Visualization

## Problem Description
This project utilizes the "Mental Health Dataset" from Kaggle, available [here](https://www.kaggle.com/datasets/divaniazzahra/mental-health-dataset). This open-source dataset provides a foundation for analyzing mental health patterns.

The goal is to construct a comprehensive data pipeline that ingests, processes, and visualizes mental health data, revealing insights across time, geography, and demographic variables to inform public health strategies.

## Project Overview
The project encompasses:

1. **Infrastructure Provisioning**: Deploy cloud resources using Terraform.
2. **Data Ingestion**: Load dataset into Google Cloud Storage (GCS).
3. **Data Transfer**: Move data from GCS to BigQuery via Airflow.
4. **Data Transformation**: Process data in BigQuery using dbt.
5. **Visualization**: Create dashboards in Power BI.

All development occurs within a GCP Virtual Machine for consistency.

## Setup Instructions

### GCP Project Configuration
1. Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin > Service Accounts** and create a new service account.
3. Generate a JSON key for the service account and download it.
4. Save the key file as `teraform-mar-0fb97fcd6586.json` in the `keys/` directory.

#### Enable APIs and Assign Roles
- Enable the **Compute Engine API**: Go to "APIs & Services" > "Library," search for "Compute Engine API," and enable it.
- Under **IAM & Admin > IAM**, assign these roles to the service account:
  - Viewer
  - Storage Admin
  - Storage Object Admin
  - BigQuery Admin
  - Compute Admin

#### SSH Key Setup
1. Generate an SSH key pair:
   ```bash
   ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048
   ```
2. Copy the public key content and paste it into **Compute Engine > Metadata > SSH Keys**.

### Terraform Deployment
Terraform automates the creation of essential cloud infrastructure. This section provides step-by-step guidance for beginners to replicate the setup.

#### Prerequisites
- Install [Terraform](https://www.terraform.io/downloads) on your local machine.
- Ensure GCP credentials are configured as above.

#### Infrastructure Components
The Terraform configuration deploys:
- **Google Cloud Storage (GCS) Bucket**: For data lake storage with automatic cleanup of incomplete uploads after 1 day.
- **BigQuery Dataset**: Named `Mar_Mental_Health_Big_Data_Project` for data warehousing.
- **GCP Virtual Machine**: An `n2-standard-4` instance in `us-central1-a` with Debian 11, tagged for the project, and equipped with a local SSD for performance.

#### Step-by-Step Deployment
1. **Navigate to the Terraform Directory**:
   ```bash
   cd Terraform/
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```
   This downloads necessary providers and sets up the working directory.

3. **Review the Plan** (Optional but Recommended):
   ```bash
   terraform plan
   ```
   This shows what resources will be created without applying changes.

4. **Apply the Configuration**:
   ```bash
   terraform apply
   ```
   - Review the proposed changes and type `yes` to confirm.
   - Terraform will create the GCS bucket, BigQuery dataset, and VM instance.

5. **Verify Resources**:
   - Check the [GCP Console](https://console.cloud.google.com/) for the new bucket, dataset, and VM.

#### Connecting to the Virtual Machine
After deployment:
1. Go to **Compute Engine > VM instances** in the GCP Console.
2. Note the **External IP** of the `mental-health-vm` instance.
3. Connect via SSH:
   ```bash
   ssh -i ~/.ssh/KEY_FILENAME USERNAME@EXTERNAL_IP
   ```
   Replace `KEY_FILENAME` and `USERNAME` with your values.

4. **Optional: Configure SSH Config** for easier access. Add to `~/.ssh/config`:
   ```bash
   Host mental-health-vm
       HostName EXTERNAL_IP
       User USERNAME
       IdentityFile ~/.ssh/KEY_FILENAME
   ```
   Then connect with:
   ```bash
   ssh mental-health-vm
   ```

### Docker Installation
Docker is essential for containerizing applications and running services like Airflow. Follow these step-by-step instructions to install Docker and Docker Compose on a fresh Debian/Ubuntu system.

1. **Update Package Index**:
   ```bash
   sudo apt update
   ```

2. **Install Prerequisites**:
   ```bash
   sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release -y
   ```

3. **Add Docker's Official GPG Key**:
   ```bash
   curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. **Add Docker Repository**:
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Install Docker and Docker Compose**:
   ```bash
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
   ```

6. **Start Docker Service**:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

7. **Add User to Docker Group**:
   ```bash
   sudo usermod -aG docker $USER
   ```
   **Note**: Log out and back in for changes to take effect.

8. **Verify Installation**:
   ```bash
   docker --version
   docker compose version
   ```

### Spark Environment Setup
This section outlines the steps to set up Java, Apache Spark, and PySpark on the GCP VM.

#### Install Java (OpenJDK)
1. Download and extract OpenJDK 11:
   ```bash
   wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
   tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
   rm openjdk-11.0.2_linux-x64_bin.tar.gz
   ```

2. Configure environment variables:
   ```bash
   export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
   export PATH="${JAVA_HOME}/bin:${PATH}"
   ```
   Add these lines to `~/.bashrc` for persistence.

#### Install Apache Spark
1. Download and unpack Spark:
   ```bash
   wget https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
   tar xzfv spark-3.5.0-bin-hadoop3.tgz
   rm spark-3.5.0-bin-hadoop3.tgz
   ```

2. Update environment variables:
   ```bash
   export SPARK_HOME="${HOME}/spark-3.5.0-bin-hadoop3"
   export PATH="${SPARK_HOME}/bin:${PATH}"
   ```
   Add these lines to `~/.bashrc` for persistence.

3. **Install GCS Connector**:
   To allow Spark to read from and write to Google Cloud Storage (`gs://` paths), download the GCS connector JAR:
   ```bash
   wget https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar
   mv gcs-connector-hadoop3-latest.jar ${SPARK_HOME}/jars/
   ```

#### Install Python, Jupyter, and Pandas
1. Install Python and Jupyter:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-pandas
   pip3 install jupyter
   ```

2. Launch PySpark with Jupyter support:
   ```bash
   PYSPARK_DRIVER_PYTHON=jupyter \
   PYSPARK_DRIVER_PYTHON_OPTS="notebook" \
   $SPARK_HOME/bin/pyspark
   ```

### Apache Airflow Installation and Configuration

This section provides detailed steps to set up Apache Airflow using Docker Compose, along with troubleshooting tips for common issues.

#### Prerequisites
- Docker and Docker Compose installed
- At least 2GB of available RAM
- Ports 8080 (Airflow UI) and 5432 (PostgreSQL) available
- **Kaggle Account**: Required for data ingestion.

#### Quick Start
1. **Navigate to the Airflow directory:**
   ```bash
   cd Apache_airflow
   ```

2. **Kaggle Configuration (Crucial for Ingestion):**
   - Place your `kaggle.json` file in `~/.kaggle/kaggle.json`.
   - **Permissions**: Ensure the directory and file are accessible by the Docker user (UID 50000):
     ```bash
     chmod 755 ~/.kaggle
     chmod 644 ~/.kaggle/kaggle.json
     ```

3. **Data Directory Permissions:**
   - Ensure the `data/` directory is world-writable so Airflow can save the downloaded files:
     ```bash
     chmod 777 ../data
     ```

4. **Start services:**
   ```bash
   docker compose up -d
   ```

5. **Access Airflow UI:**
   - URL: http://localhost:8080
   - Username: `admin`
   - Password: `admin`

#### Kaggle Data Ingestion Setup

The project includes an automated pipeline to fetch the "Mental Health Dataset" directly from Kaggle.

##### 1. Docker Compose Configuration
The `docker-compose.yml` is configured to:
- **Install Dependencies**: Automatically installs `kaggle` and `pandas` at runtime using:
  ```yaml
  _PIP_ADDITIONAL_REQUIREMENTS: "kaggle pandas"
  ```
- **Volume Mounts**: Maps local directories for persistent storage and configuration:
  ```yaml
  volumes:
    - ../data:/opt/airflow/data               # For downloaded datasets
    - ~/.kaggle:/home/airflow/.kaggle          # For Kaggle API credentials
  ```

##### 2. Automated Ingestion Script (`ingestion script.ipynb`)
For manual testing or initial exploration, a Jupyter notebook is provided with a reusable function:
```python
from kaggle.api.kaggle_api_extended import KaggleApi

def download_kaggle_dataset(dataset, download_path='./data'):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(dataset, path=download_path, unzip=True, force=True)
```

##### 3. Airflow DAG (`kaggle_ingestion_dag`)
Located in `Apache_airflow/dags/mental_health_etl.py`, this DAG automates the daily ingestion:
- **`download_from_kaggle`**: Authenticates and downloads the latest ZIP file, extracting it to `/opt/airflow/data`.
- **`process_and_verify_data`**: Uses `pandas` to read the CSV and log data statistics (row/column counts) to ensure the file is valid.

#### Directory Structure
```
.
├── ingestion script.ipynb    # Manual ingestion & testing
├── data/                     # Host directory for datasets (mounted to /opt/airflow/data)
└── Apache_airflow/
    ├── docker-compose.yml    # Orchestration & Volume setup
    ├── dags/                 # Airflow DAGs
    │   └── mental_health_etl.py # Kaggle ETL Pipeline
    ├── logs/                 # Task execution logs
    └── plugins/              # Custom plugins
```

#### Troubleshooting

1. **Permission Denied (Kaggle API):**
   - If the task fails with `Missing username in configuration`, verify `~/.kaggle/kaggle.json` is world-readable (`chmod 644`) and the mount in `docker-compose.yml` is correct.

2. **Permission Denied (Data Folder):**
   - If `pandas` or `kaggle` cannot write to `/opt/airflow/data`, run `chmod 777 data/` on the host machine.

3. **ModuleNotFoundError (kaggle/pandas):**
   - These are installed on startup. If missing, restart the containers: `docker compose down && docker compose up -d`.

4. **DAG not appearing:**
   - Airflow can take up to 60 seconds to parse new files. Refresh the UI and ensure no filters (like "Active") are hiding the `kaggle_ingestion_dag`.

#### Service Health Check
```bash
# Check service status
docker compose ps

# Check PostgreSQL
docker compose exec postgres pg_isready -U airflow -d airflow

# Check Airflow webserver
curl http://localhost:8080/health
```

## Advanced Configuration: Integrating Airflow (Docker) with Local Spark & GCP

To achieve a fully automated pipeline that leverages high-performance processing, this project uses a hybrid architecture where **Apache Airflow runs in Docker** while utilizing **Spark and Java installed on the host Linux machine**.

### 1. Hybrid Environment Architecture
*   **Host Machine**: Houses the Spark 3.5.0 binaries and OpenJDK 11. This allows for persistent management of Spark configurations and JARs (like the GCS connector).
*   **Docker Containers**: Airflow services (Webserver, Scheduler, Init) run in isolated containers but access the host's Spark and Java through high-performance volume mounts.

### 2. Dependency Management
To enable the `mental_health_full_pipeline` DAG, the following dependencies are automatically managed:
*   **PIP Requirements**: `pyspark`, `kaggle`, and `pandas` are injected into the containers at runtime via the `_PIP_ADDITIONAL_REQUIREMENTS` variable in `docker-compose.yml`.
*   **Spark-GCS Connectivity**: The `gcs-connector-hadoop3-latest.jar` is placed in the host's Spark `jars/` directory, making it available to the containerized Airflow workers.

### 3. Critical Volume Mounts (`docker-compose.yml`)
The following mappings were established to bridge the Host and Docker environments:
| Host Path | Container Path | Purpose |
| :--- | :--- | :--- |
| `~/spark-3.5.0-bin-hadoop3` | `/usr/local/spark` | Provides Spark binaries and PySpark libraries. |
| `~/jdk-11.0.2` | `/usr/local/openjdk-11` | Provides Java runtime required by Spark. |
| `../key` | `/opt/airflow/key` | Grants access to GCP Service Account JSON keys. |
| `~/.kaggle` | `/home/airflow/.kaggle` | Grants access to Kaggle API credentials. |

### 4. Environment Configuration & Troubleshooting
Several key configurations were implemented to ensure smooth execution:

*   **PATH Resolution**: A customized `PATH` was set inside the containers to include `/usr/local/spark/bin` and `/usr/local/openjdk-11/bin` while preserving the default Airflow binary paths. This fixed the "airflow: command not found" error encountered during initial setup.
*   **PySpark Integration**: `PYTHONPATH` was configured to point to `/usr/local/spark/python` and the necessary `py4j` source ZIPs, allowing Airflow's Python interpreter to import `pyspark` correctly.
*   **GCP Authentication**: The `GOOGLE_APPLICATION_CREDENTIALS` variable was added to the Airflow environment, pointing to the mounted key path. This allows GCP Operators (like `GCSToBigQueryOperator`) to authenticate without manual connection setup in the UI.
*   **Java Runtime**: By mounting the host's JDK and setting `JAVA_HOME`, we resolved the `java: command not found` errors that typically occur when running Spark jobs in standard Airflow images.


Dag running spark, python uploading data to gcp and bigquery
![air_flow Dag](images/airflow_orchestration.png)


## Next Steps
With infrastructure in place, proceed to:
- Data ingestion using python, spark 
- Workflow orchestration with Airflow.
- Data transformation via dbt.
- Dashboard creation in Power BI.

 Installing dbt-core and Adapters
With the virtual environment activated, install dbt-core along with the dbt-bigquery and dbt-duckdb adapters.

pip install dbt-core dbt-bigquery dbt-duckdb

Refer to individual tool documentation for detailed implementation.

## dbt Core Setup and BigQuery Configuration

This project uses dbt (data build tool) for transforming raw data in BigQuery into analytical models.

### 1. Installation of dbt Core and BigQuery Adapter

It is recommended to use a Python virtual environment to manage dbt and its adapters.

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dbt Core and the BigQuery adapter
pip install dbt-core dbt-bigquery
```

### 2. Confirming Installation

Verify that dbt and the BigQuery adapter are correctly installed:

```bash
dbt --version
```
You should see `Core: 1.x.x` and `bigquery: 1.x.x` in the output.

### 3. VS Code Extensions for dbt

For an optimized development experience, install these extensions:
- **dbt Power User**: Highly recommended for model lineage, real-time query validation, and compiled SQL preview.
- **dbt**: Basic syntax highlighting and support.

### 4. Configuring dbt to Connect to BigQuery

dbt uses a `profiles.yml` file to store connection details. This file is typically located at `~/.dbt/profiles.yml` or `C:\Users\<User>\.dbt\profiles.yml`.

#### Service Account Key
The project uses a Service Account JSON key for authentication, located at:
`DE_PROJECT1/Terraform/keys/teraform-mar-0fb97fcd6586.json`

#### profiles.yml Configuration
Update your `profiles.yml` with the following:

```yaml
mental_health_data:
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: teraform-mar
      dataset: mental_health_data
      threads: 1
      keyfile: C:\Users\amben\Desktop\Mentel_Health_Project\DE_PROJECT1\Terraform\keys\teraform-mar-0fb97fcd6586.json
      location: US
      priority: interactive
      job_execution_timeout_seconds: 300
      job_retries: 1
  target: dev
```

### 5. Verifying the Connection

Navigate to the dbt project directory (`DE_PROJECT1/dbt/mental_health_data`) and run:

```bash
dbt debug
```
A successful connection will show `Connection test: [OK connection ok]`.

### 6. Working with Data Sources

The raw data sources are defined in `models/sources.yml`. To pull data from the raw BigQuery dataset and create your first staging model:

```bash
# Run the staging model
dbt run --select stg_mental_health
```

---

## dbt Implementation Details

### 7. dbt Project Structure and Models

The dbt project is organized as follows:

```
dbt/mental_health_data/
├── dbt_project.yml                 # Project configuration
├── models/
│   ├── example/
│   │   ├── my_first_dbt_model.sql
│   │   ├── my_second_dbt_model.sql
│   │   └── schema.yml
│   ├── staging/
│   │   ├── stg_mental_health.sql   # Primary staging model
│   │   └── sources.yml             # Data source definitions
│   ├── intermediate/               # (Placeholder for intermediate transformations)
│   └── marts/
│       └── fct_mental_health_analysis.sql  # Fact table with analytical dimensions
├── macros/                         # Custom dbt macros
├── tests/                          # Data quality tests
├── seeds/                          # Static data files
└── logs/                           # Execution logs
```

#### Models Description

1. **Staging Model (`stg_mental_health.sql`)**
   - **Type**: View
   - **Purpose**: Cleans and standardizes raw mental health data from BigQuery
   - **Source**: `raw_mental_health.mental_health_data` table
   - **Columns**: All columns from raw data (Timestamp, Gender, Country, Occupation, etc.)
   - **Operations**: Simple transformation using `SELECT *` to pull data from source

2. **Fact Table Model (`fct_mental_health_analysis.sql`)**
   - **Type**: Table (Default materialization)
   - **Purpose**: Creates an analytical fact table with curated columns and cleaned naming conventions
   - **Dependencies**: References `stg_mental_health` staging model
   - **Key Dimensions**:
     - `created_at` (from Timestamp)
     - `gender`, `country`, `occupation`
     - `self_employed` status
   - **Mental Health Indicators**:
     - Family history, treatment status
     - Days indoors, growing stress levels
     - Habit changes, mental health history
     - Mood swings, coping struggles
     - Work interest, social weakness
     - Interview responses, care options
   - **Output**: Ready for visualization and analysis in Power BI

### 8. Running dbt Models

#### Run All Models
```bash
cd C:\Users\amben\Desktop\Mentel_Health_Project\DE_PROJECT1\dbt\mental_health_data
dbt run
```

#### Run Specific Models
```bash
# Run only the staging model
dbt run --select stg_mental_health

# Run only the fact table model
dbt run --select fct_mental_health_analysis
```

#### Compile Models (Without Executing)
```bash
dbt compile
```

#### Generate Documentation
```bash
dbt docs generate
dbt docs serve  # Opens documentation UI on localhost:8000
```

### 9. Accessing Transformed Data in BigQuery

After running dbt models, the transformed data is available in BigQuery:

**Dataset**: `mental_health_data` (in project `teraform-mar`)

**Tables/Views Created**:
- `my_first_dbt_model` (Table)
- `stg_mental_health` (View)
- `my_second_dbt_model` (View)
- `fct_mental_health_analysis` (Table)

**Access Methods**:

1. **BigQuery Console** (Web UI):
   - Navigate to [Google Cloud Console](https://console.cloud.google.com/)
   - Go to BigQuery > Projects > `teraform-mar` > Dataset > `mental_health_data`
   - View tables and execute SQL queries

2. **Query in BigQuery**:
   ```sql
   SELECT * FROM `teraform-mar.mental_health_data.fct_mental_health_analysis` LIMIT 10;
   ```

3. **Connect from Power BI**:
   - Create a new data source: BigQuery connector
   - Project: `teraform-mar`
   - Dataset: `mental_health_data`
   - Select tables for visualization

### 10. Automating dbt Jobs to Run Daily

dbt can be automated to run on a schedule using several approaches:

#### Option 1: Using dbt Cloud (Recommended for Production)

dbt Cloud provides a fully managed solution with scheduling, logging, and monitoring:

1. **Sign Up**: Create an account at [dbt Cloud](https://cloud.getdbt.com/)

2. **Connect Repository**:
   - Link your GitHub/GitLab repository containing the dbt project
   - Authorize dbt Cloud to access your repository

3. **Create dbt Cloud Job**:
   - Click "New Job" → "Deploy Job"
   - Select your project and environment
   - Command: `dbt run`
   - Set schedule: Daily at a specific time (e.g., 2:00 AM UTC)

4. **Configure Notifications** (Optional):
   - Slack notifications on job success/failure
   - Email alerts

#### Option 2: Using Apache Airflow (Recommended for Hybrid Setup)

Since your project already uses Airflow, add a dbt task to the pipeline:

1. **Create Airflow DAG** (`Apache_airflow/dags/dbt_transformation_dag.py`):
   ```python
   from airflow import DAG
   from airflow.operators.bash import BashOperator
   from datetime import datetime, timedelta

   default_args = {
       'owner': 'data-engineering',
       'retries': 2,
       'retry_delay': timedelta(minutes=5),
       'start_date': datetime(2024, 1, 1),
   }

   dag = DAG(
       'daily_dbt_transformation',
       default_args=default_args,
       description='Run dbt models daily',
       schedule_interval='0 2 * * *',  # 2 AM UTC every day
       catchup=False,
   )

   dbt_run = BashOperator(
       task_id='run_dbt_models',
       bash_command="""
           cd /path/to/dbt/mental_health_data && \
           source .venv/bin/activate && \
           dbt run --profiles-dir ~/.dbt
       """,
       dag=dag,
   )

   dbt_test = BashOperator(
       task_id='test_dbt_models',
       bash_command="""
           cd /path/to/dbt/mental_health_data && \
           source .venv/bin/activate && \
           dbt test --profiles-dir ~/.dbt
       """,
       dag=dag,
   )

   dbt_run >> dbt_test
   ```

2. **Deploy in Airflow**:
   - Copy the DAG file to `Apache_airflow/dags/`
   - Refresh Airflow UI to register the DAG
   - Enable the DAG and it will run automatically according to schedule

3. **Monitor Execution**:
   - View DAG runs in Airflow UI at http://localhost:8080
   - Check logs for any failures

#### Option 3: Using a Cron Job (Linux/Windows Task Scheduler)

For simple scheduling without a full orchestration tool:

**On Linux**:
```bash
# Edit crontab
crontab -e

# Add this line to run dbt daily at 2 AM
0 2 * * * cd /path/to/dbt/mental_health_data && /path/to/.venv/bin/dbt run
```

**On Windows (Task Scheduler)**:
1. Open Task Scheduler
2. Create Basic Task → Set trigger to "Daily"
3. Set time to 2:00 AM
4. Action: Start a program
5. Program: `C:\Users\amben\.venv\Scripts\python.exe`
6. Arguments: `-m dbt.cli run`
7. Start in: `C:\Users\amben\Desktop\Mentel_Health_Project\DE_PROJECT1\dbt\mental_health_data`

#### Option 4: Using GitHub Actions (CI/CD)

Automate dbt runs via GitHub Actions on schedule:

1. **Create Workflow File** (`.github/workflows/dbt-run.yml`):
   ```yaml
   name: Daily dbt Run
   on:
     schedule:
       - cron: '0 2 * * *'  # Run daily at 2 AM UTC
   
   jobs:
     dbt-run:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.10'
         - name: Install dbt
           run: |
             pip install dbt-core dbt-bigquery
         - name: Configure dbt
           run: |
             mkdir -p ~/.dbt
             echo "${{ secrets.DBT_PROFILES_YML }}" > ~/.dbt/profiles.yml
         - name: Run dbt
           run: |
             cd dbt/mental_health_data
             dbt run
   ```

2. **Add Secrets**:
   - GitHub Repo → Settings → Secrets
   - Add `DBT_PROFILES_YML` with your `profiles.yml` content
   - Add `GCP_SERVICE_ACCOUNT_KEY` for BigQuery authentication

### 11. Monitoring and Troubleshooting

#### View dbt Logs
```bash
# Logs are stored in the dbt project
ls -la dbt/mental_health_data/logs/

# View run results
cat dbt/mental_health_data/target/run_results.json
```

#### Common Issues

1. **Connection Errors**:
   ```bash
   dbt debug
   ```
   Ensures all configurations and connections are valid.

2. **Model Compilation Errors**:
   - Check SQL syntax in model files
   - Ensure all referenced sources exist in BigQuery
   - Validate column names and data types

3. **Permission Issues**:
   - Verify service account has `BigQuery Admin` and `Storage Admin` roles in GCP
   - Check that `dbt_project.yml` and `profiles.yml` paths are correct

4. **Performance Issues**:
   - Monitor BigQuery job execution times
   - Use dbt's `--threads` parameter to adjust concurrency:
     ```bash
     dbt run --threads 4
     ```

the linage in Dbt
![dbt lineage](images/dbt_lineage.png)


Visualization in Power BI
connection to dbt fact table in big query using the big query connection in power BI
and generation of charts

![Power BI report](images/powerbi_report.png)


