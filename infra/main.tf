terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
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
