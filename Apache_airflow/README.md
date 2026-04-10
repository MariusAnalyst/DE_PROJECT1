# Apache Airflow Docker Setup

This directory contains a minimal, production-ready Docker Compose setup for running Apache Airflow with PostgreSQL as the metadata database.

## Architecture

The setup includes the following services:
- **PostgreSQL 13**: Metadata database for Airflow (stores DAGs, task history, connections)
- **Airflow Webserver**: Web UI for managing DAGs and monitoring task execution
- **Airflow Scheduler**: Schedules and triggers DAG runs

Uses **LocalExecutor** for simplicity - tasks run sequentially on the scheduler container.

## Prerequisites

- Docker and Docker Compose installed
- At least 2GB of available RAM
- Port 8080 (Airflow UI) and 5432 (PostgreSQL) available
- **Java 11** and **Apache Spark 3.5.0** (installed manually)

## Manual Installations (Java & Spark)

To support Spark-based DAGs and processing, Java and Spark were installed manually in the home directory.

### Installation Steps

1. **Java JDK 11**:
   - Downloaded and placed in `${HOME}/jdk-11.0.2`.
2. **Apache Spark 3.5.0**:
   - Downloaded `spark-3.5.0-bin-hadoop3.tgz` to `${HOME}`.
   - Extracted using: `tar -xzf ~/spark-3.5.0-bin-hadoop3.tgz -C ~/`.

### System Configuration Changes

The following environment variables were added to `~/.bashrc` to make the binaries accessible system-wide:

```bash
export JAVA_HOME="${HOME}/jdk-11.0.2"
export SPARK_HOME="${HOME}/spark-3.5.0-bin-hadoop3"
export PATH="${JAVA_HOME}/bin:${SPARK_HOME}/bin:${PATH}"
```

To apply these changes in your current session, run:
```bash
source ~/.bashrc
```

Verification:
```bash
java -version
spark-shell --version
```

## Quick Start

1. **Navigate to this directory:**
   ```bash
   cd Apache_airflow
   ```

2. **Start services:**
   ```bash
   docker compose up -d
   ```

3. **Wait for startup** (30-60 seconds for initialization)

4. **Access Airflow UI:**
   - URL: http://localhost:8080
   - Username: `admin`
   - Password: `admin`

5. **Stop services:**
   ```bash
   docker compose down
   ```

## Directory Structure

```
Apache_airflow/
├── docker-compose.yml    # Docker Compose configuration
├── dags/                 # Airflow DAGs directory
│   └── sample_dag.py     # Sample DAG for testing
├── logs/                 # Airflow task logs
└── plugins/              # Custom Airflow plugins
```

## Configuration

### Environment Variables

Key configuration in `docker-compose.yml`:

- **Executor**: LocalExecutor (simple, single-machine execution)
- **Database**: PostgreSQL with user `airflow`, password `airflow`
- **Admin User**: `admin` / `admin` (change in production)
- **Fernet Key**: Used for encryption

### Security Notes

⚠️ **For Production**:
- Change default passwords
- Use environment variables for secrets
- Configure proper authentication and SSL/TLS
- Use external managed database
- Set up monitoring and alerting

## Usage

### Adding DAGs

Place your DAG Python files in the `dags/` directory. Airflow automatically detects and loads them.

Example structure:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def my_task():
    print("Task executed!")

dag = DAG('my_dag', start_date=datetime(2024, 1, 1))
task = PythonOperator(task_id='task_1', python_callable=my_task, dag=dag)
```

### Viewing Logs

```bash
# View all service logs
docker compose logs

# View specific service logs
docker compose logs airflow-webserver
docker compose logs airflow-scheduler

# Follow logs in real-time
docker compose logs -f airflow-scheduler
```

### Database Operations

```bash
# Access PostgreSQL directly
docker compose exec postgres psql -U airflow -d airflow

# Reset database (⚠️ destroys all data and task history)
docker compose down -v
docker compose up -d
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8080 and 5432 are available
   ```bash
   # Check port availability
   lsof -i :8080
   lsof -i :5432
   ```

2. **Memory issues**: LocalExecutor needs less RAM than distributed setups, minimum 2GB

3. **DAG not appearing**: 
   - Check DAG syntax: `python dags/your_dag.py`
   - Verify file is in `dags/` directory
   - Check scheduler logs: `docker compose logs airflow-scheduler`

4. **Connection refused**: Wait longer for PostgreSQL to be ready
   ```bash
   docker compose ps  # Check service health
   ```

5. **Permission issues**: Ensure Docker has proper permissions
   ```bash
   sudo usermod -aG docker $USER
   ```

### Service Health Check

```bash
# Check service status
docker compose ps

# Check PostgreSQL
docker compose exec postgres pg_isready -U airflow -d airflow

# Check Airflow webserver
curl http://localhost:8080/health
```

## Airflow 3.0 Migration & Troubleshooting

### Login Issues (Authentication Manager)

**Issue:** In Airflow 3.0, the default `SimpleAuthManager` was introduced, which generates random passwords and does not support the traditional `_AIRFLOW_WWW_USER_CREATE` environment variables.

**Resolution:** 
To use the traditional `admin/admin` login, the `FabAuthManager` (from the FAB provider) must be explicitly configured in `docker-compose.yml`:

1. **Set the Auth Manager:**
   ```yaml
   AIRFLOW__CORE__AUTH_MANAGER: airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
   ```
2. **Use the correct command:**
   The `webserver` command is deprecated in 3.0. Use `api-server` instead:
   ```yaml
   command: api-server
   ```
3. **Reset if necessary:**
   If you switched managers and are seeing `500 Internal Server Error` or database transaction aborts, perform a clean reset (this wipes the metadata DB but keeps your mapped DAGs):
   ```bash
   docker compose down -v
   docker compose up -d
   ```

### Reset Everything

Complete reset (⚠️ deletes all data):

```bash
# Stop and remove all containers and volumes
docker compose down -v --remove-orphans

# Remove all images
docker rmi apache/airflow:2.9.0 postgres:13

# Restart
docker compose up -d
```

## Development

### Adding Custom Python Packages

Edit `requirements.txt` and the Airflow image will load them on startup:

```dockerfile
# Dockerfile (if building custom image)
FROM apache/airflow:2.9.0
RUN pip install --no-cache-dir requests pandas google-cloud-bigquery
```

Or mount requirements during runtime in `docker-compose.yml`.

## Limitations & Scaling

**LocalExecutor** suitable for:
- Development and testing
- Small to medium workloads (< 1000 tasks/day)
- Sequential task execution

**For larger deployments**, upgrade to:
- **CeleryExecutor**: Distributed task execution across multiple workers
- **KubernetesExecutor**: Run tasks in Kubernetes pods
- **Managed Airflow**: Use cloud services (GCP Cloud Composer, AWS MWAA, etc.)

## Next Steps

1. Create your DAGs in `dags/` directory
2. Set up Airflow connections (Admin > Connections) for external systems
3. Configure variables and secrets (Admin > Variables)
4. Monitor task execution in the UI
5. Set up email/Slack alerts for failures