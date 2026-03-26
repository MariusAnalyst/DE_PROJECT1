# Mental Health Data Pipeline Project

## Table of Contents
- [Objective](#objective)
- [Technologies Used](#technologies-used)
- [Problem Description](#problem-description)
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [Terraform Deployment](#terraform-deployment)
- [Next Steps](#next-steps)

## Objective
**Unlocking Insights into Mental Health: Building a Robust Data Pipeline for Global Analysis**

Transform raw mental health data into actionable visualizations, empowering stakeholders to identify trends, geographic patterns, and temporal shifts in mental well-being across populations.

## Technologies Used
This project leverages cutting-edge cloud and data engineering tools:

- [<img src="https://www.terraform.io/img/terraform-logo.png" alt="Terraform" width="50"/> Terraform](https://www.terraform.io/docs) - Infrastructure as Code
- [<img src="https://icons8.com/icons/set/google-cloud" alt="Google Cloud Platform" width="50"/> Google Cloud Platform (GCP)](https://cloud.google.com/docs) - Cloud Services
- [<img src="https://airflow.apache.org/docs/apache-airflow/stable/_images/pin_large.png" alt="Apache Airflow" width="50"/> Apache Airflow](https://airflow.apache.org/docs/) - Workflow Orchestration
- [<img src="https://cloud.google.com/images/products/bigquery.png" alt="BigQuery" width="50"/> Google BigQuery](https://cloud.google.com/bigquery/docs) - Data Warehouse
- [<img src="https://docs.getdbt.com/img/dbt-logo.png" alt="dbt" width="50"/> dbt](https://docs.getdbt.com/) - Data Transformation
- [<img src="https://powerbi.microsoft.com/pictures/application-logos/svg/powerbi.svg" alt="Power BI" width="50"/> Power BI](https://docs.microsoft.com/en-us/power-bi/) - Data Visualization

## Problem Description
This Project utilizes the "Mental Health Dataset" from Kaggle, available [here](https://www.kaggle.com/datasets/divaniazzahra/mental-health-dataset). This open-source dataset provides a foundation for analyzing mental health patterns.

The goal is to construct a comprehensive data pipeline that ingests, processes, and visualizes mental health data, revealing insights across time, geography, and demographic variables to inform public health strategies.

## Project Overview
The project encompasses:

1. **Infrastructure Provisioning**: Deploy cloud resources using Terraform
2. **Data Ingestion**: Load dataset into Google Cloud Storage (GCS)
3. **Data Transfer**: Move data from GCS to BigQuery via Airflow
4. **Data Transformation**: Process data in BigQuery using dbt
5. **Visualization**: Create dashboards in Power BI

All development occurs within a GCP Virtual Machine for consistency.

## Setup Instructions
### GCP Project Configuration
1. Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **IAM & Admin > Service Accounts** and create a new service account.
3. Generate a JSON key for the service account and download it.
4. Save the key file as `teraform-mar-0fb97fcd6586.json` in the `keys/` directory.

### Enable APIs and Assign Roles
- Enable the **Compute Engine API**: Go to "APIs & Services" > "Library," search for "Compute Engine API," and enable it.
- Under **IAM & Admin > IAM**, assign these roles to the service account:
  - Viewer
  - Storage Admin
  - Storage Object Admin
  - BigQuery Admin
  - Compute Admin

### SSH Key Setup
1. Generate an SSH key pair:
   ```
   ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048
   ```
2. Copy the public key content and paste it into **Compute Engine > Metadata > SSH Keys**.

## Terraform Deployment
Terraform automates the creation of essential cloud infrastructure. This section provides step-by-step guidance for beginners to replicate the setup.

### Prerequisites
- Install [Terraform](https://www.terraform.io/downloads) on your local machine.
- Ensure GCP credentials are configured as above.

### Infrastructure Components
The Terraform configuration deploys:
- **Google Cloud Storage (GCS) Bucket**: For data lake storage with automatic cleanup of incomplete uploads after 1 day.
- **BigQuery Dataset**: Named `Mar_Mental_Health_Big_Data_Project` for data warehousing.
- **GCP Virtual Machine**: An `n2-standard-4` instance in `us-central1-a` with Debian 11, tagged for the project, and equipped with a local SSD for performance.

### Step-by-Step Deployment
1. **Navigate to the Terraform Directory**:
   ```
   cd Terraform/
   ```

2. **Initialize Terraform**:
   ```
   terraform init
   ```
   This downloads necessary providers and sets up the working directory.

3. **Review the Plan** (Optional but Recommended):
   ```
   terraform plan
   ```
   This shows what resources will be created without applying changes.

4. **Apply the Configuration**:
   ```
   terraform apply
   ```
   - Review the proposed changes and type `yes` to confirm.
   - Terraform will create the GCS bucket, BigQuery dataset, and VM instance.

5. **Verify Resources**:
   - Check the [GCP Console](https://console.cloud.google.com/) for the new bucket, dataset, and VM.

### Connecting to the Virtual Machine
After deployment:
1. Go to **Compute Engine > VM instances** in the GCP Console.
2. Note the **External IP** of the `mental-health-vm` instance.
3. Connect via SSH:
   ```
   ssh -i ~/.ssh/KEY_FILENAME USERNAME@EXTERNAL_IP
   ```
   Replace `KEY_FILENAME` and `USERNAME` with your values.

4. **Optional: Configure SSH Config** for easier access. Add to `~/.ssh/config`:
   ```
   Host mental-health-vm
       HostName EXTERNAL_IP
       User USERNAME
       IdentityFile ~/.ssh/KEY_FILENAME
   ```
   Then connect with:
   ```
   ssh mental-health-vm
   ```

### Installing Docker on the VM
Docker is essential for containerizing applications and running services like Airflow. Follow these step-by-step instructions to install Docker and Docker Compose on a fresh Debian/Ubuntu system.

#### Step 1: Update Package Index
First, update your package index to ensure you have the latest package information:
```bash
sudo apt update
```

#### Step 2: Install Prerequisites
Install the necessary packages for adding Docker's official repository:
```bash
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release -y
```

#### Step 3: Add Docker's Official GPG Key
Download and add Docker's official GPG key to verify package authenticity:
```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

#### Step 4: Add Docker Repository
Add Docker's official repository to your system's package sources:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

#### Step 5: Update Package Index Again
Update the package index to include the new Docker repository:
```bash
sudo apt update
```

#### Step 6: Install Docker Engine and Docker Compose
Install Docker Engine, CLI, containerd, and Docker Compose plugin:
```bash
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

#### Step 7: Start Docker Service
Start the Docker service:
```bash
sudo systemctl start docker
```

#### Step 8: Enable Docker to Start on Boot
Configure Docker to start automatically when the system boots:
```bash
sudo systemctl enable docker
```

#### Step 9: Add User to Docker Group (Optional but Recommended)
Add your user to the docker group to run Docker commands without sudo:
```bash
sudo usermod -aG docker $USER
```

**Note:** After running this command, log out and back in for the group changes to take effect.

#### Step 10: Verify Installation
Verify that Docker and Docker Compose are installed correctly:
```bash
docker --version
docker compose version
```

#### Step 11: Test Docker Installation
Run a test container to ensure Docker is working properly:
```bash
sudo docker run hello-world
```

You should see a "Hello from Docker!" message confirming successful installation.

**Troubleshooting:**
- If you get permission errors, ensure you've logged out and back in after adding yourself to the docker group
- If Docker commands still require sudo, run: `newgrp docker` in your terminal session
- For any installation issues, refer to the [official Docker documentation](https://docs.docker.com/engine/install/debian/)

7. Clone the Repository:
   ```
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   ```
   Replace with your repository URL.

### Cleanup
To destroy all resources:
```
terraform destroy
```
Confirm with `yes`. This removes the VM, bucket, and dataset.

## Next Steps
With infrastructure in place, proceed to:
- Data ingestion using Mage
- Workflow orchestration with Airflow
- Data transformation via dbt
- Dashboard creation in Power BI

Refer to individual tool documentation for detailed implementation.
