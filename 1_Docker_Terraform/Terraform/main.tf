terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "gcp_bucket_1" {
  name                     = "dezoomcamp2024-412618_demo-bucket-1"
  location                 = var.location
  force_destroy            = true
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"
}

resource "google_storage_bucket" "gcp_bucket_2" {
  name                     = "dezoomcamp2024-412618_demo-bucket-2"
  location                 = var.region
  force_destroy            = true
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"
}
