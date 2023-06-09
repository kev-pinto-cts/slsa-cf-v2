terraform {
  required_version = ">= 1.3.1"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.55.0" # tftest
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 4.55.0" # tftest
    }
  }
}

terraform {
  backend "gcs" {
    bucket = "terraform-state-305379539480"
    prefix = "terraform/state"
  }
}
