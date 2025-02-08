terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  # backend "s3" {
  #   endpoints = {
  #     s3 = "https://storage.yandexcloud.net"
  #   }
  #   bucket = "trade-helper-internal"
  #   region = "ru-central1"
  #   key    = "terraform.tfstate"
  #
  #   skip_region_validation      = true
  #   skip_credentials_validation = true
  #   skip_requesting_account_id = true
  #   # This option is required to describe a backend for Terraform version 1.6.1 or higher.
  #   skip_s3_checksum            = true
  #   # This option is required to describe a backend for Terraform version 1.6.3 or higher.
  #
  # }
  required_version = ">= 0.13"
}

provider "yandex" {
  token    = var.token
  cloud_id = var.cloud_id
  zone     = local.zone
}


data "yandex_resourcemanager_folder" "default" {
  name = "default"
  cloud_id = var.cloud_id
}


data "yandex_ydb_database_serverless" "ydb" {
  name = "ydb"
  folder_id = data.yandex_resourcemanager_folder.default.folder_id
}

output "ydb-url" {
  value = data.yandex_ydb_database_serverless.ydb.ydb_full_endpoint
}

locals {
  resource_prefix = "${local.project_name}"
  zone            = "ru-central1-a"
  project_name    = "auth-sevice"
}
