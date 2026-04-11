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

