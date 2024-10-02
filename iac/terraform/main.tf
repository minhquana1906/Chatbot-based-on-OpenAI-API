terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.80.0" 
    }
  }
  required_version = "1.9.5" 
}

provider "google" {
  project     = var.project_id
  region      = var.region
}

// Google Kubernetes Engine
resource "google_container_cluster" "primary" {
  name     = "${var.project_id}-gke"
  location = var.zone

  // Enabling Autopilot for this cluster
  enable_autopilot = false

  // Specify the initial number of nodes
  initial_node_count = 2

  // Node configuration
  node_config {
    machine_type = "e2-standard-2" 
    disk_size_gb = 30
  }
}

resource "google_storage_bucket" "loki-bucket" {
  name          = var.bucket-loki
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "tempo-bucket" {
  name          = var.bucket-tempo
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

# resource "google_storage_bucket" "prometheus-bucket" {
#   name          = var.bucket-prometheus
#   location      = var.region
#   force_destroy = true

#   uniform_bucket_level_access = true
# }
