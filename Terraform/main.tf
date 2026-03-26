terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.25.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file_path)
  project = "teraform-mar"
  region  = "us-central1"
}

resource "google_storage_bucket" "auto-expire" {
  name          = var.gcs_bucket_name
  location      = var.gcs_location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "mental_health_dataset" {
  dataset_id = var.big_data_name
}



resource "google_compute_instance" "default" {
  name         = "mental-health-vm"
  # Fix: Changed from e2-standard-4 to n2-standard-4 to support Local SSD
  machine_type = "n2-standard-4"
  zone         = "us-central1-a"

  tags = ["data-engine", "mental-health-project"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = {
        environment = "dev"
      }
    }
  }

  # Local SSD disk - Now compatible with N2 machine type
  scratch_disk {
    interface = "NVME"
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    project = "mental-health-analysis"
  }
}