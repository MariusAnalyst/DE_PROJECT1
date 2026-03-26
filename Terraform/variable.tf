variable "credentials_file_path" {
  type        = string
  default     = "C:/Users/amben/Desktop/DE_PROJECT1/keys/teraform-mar-0fb97fcd6586.json"
  description = "Path to the GCP credentials JSON file"
}



variable "big_data_name" {
  type        = string
  default     = "Mar_Mental_Health_Big_Data_Project"
  description = "My big query dataset name"
}

variable "gcs_storage_class" {
  type        = string
  default     = "STANDARD"
  description = "My storage bucket class"
}

variable "gcs_location" {
  type        = string
  default     = "US"
  description = "My storage bucket location"
}

variable "gcs_bucket_name" {
  type        = string
  default     = "mar_mental_health_bucket"
  description = "My storage bucket name"
}