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
- [Next Steps](#next-steps)

## Objective
**Unlocking Insights into Mental Health: Building a Robust Data Pipeline for Global Analysis**

Transform raw mental health data into actionable visualizations, empowering stakeholders to identify trends, geographic patterns, and temporal shifts in mental well-being across populations.

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
   export SPARK_HOME="${HOME}/spark/spark-3.5.0-bin-hadoop3"
   export PATH="${SPARK_HOME}/bin:${PATH}"
   ```
   Add these lines to `~/.bashrc` for persistence.

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

#### Quick Start
1. **Navigate to the Airflow directory:**
   ```bash
   cd Apache_airflow
   ```

2. **Start services:**
   ```bash
   docker compose up -d
   ```

3. **Access Airflow UI:**
   - URL: http://localhost:8080
   - Username: `admin`
   - Password: `admin`

4. **Stop services:**
   ```bash
   docker compose down
   ```

#### Directory Structure
```
Apache_airflow/
├── docker-compose.yml    # Docker Compose configuration
├── dags/                 # Airflow DAGs directory
│   └── sample_dag.py     # Sample DAG for testing
├── logs/                 # Airflow task logs
└── plugins/              # Custom Airflow plugins
```

#### Troubleshooting

1. **Port conflicts:** Ensure ports 8080 and 5432 are available.
   ```bash
   lsof -i :8080
   lsof -i :5432
   ```

2. **DAG not appearing:**
   - Check DAG syntax: `python dags/your_dag.py`
   - Verify file is in `dags/` directory
   - Check scheduler logs: `docker compose logs airflow-scheduler`

3. **Connection refused:** Wait longer for PostgreSQL to be ready.
   ```bash
   docker compose ps  # Check service health
   ```

4. **Permission issues:** Ensure Docker has proper permissions.
   ```bash
   sudo usermod -aG docker $USER
   ```

#### Service Health Check
```bash
# Check service status
docker compose ps

# Check PostgreSQL
docker compose exec postgres pg_isready -U airflow -d airflow

# Check Airflow webserver
curl http://localhost:8080/health
```

## Next Steps
With infrastructure in place, proceed to:
- Data ingestion using Mage.
- Workflow orchestration with Airflow.
- Data transformation via dbt.
- Dashboard creation in Power BI.

Refer to individual tool documentation for detailed implementation.
