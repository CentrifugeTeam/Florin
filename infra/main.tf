terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  token     = var.token
  cloud_id  = var.cloud_id
  zone      = local.zone
  folder_id = var.folder_id
}


resource "yandex_ydb_database_serverless" "ydb" {
  name = "ydb"
}



locals {
  resource_prefix = "${local.project_name}"
  zone            = "ru-central1-a"
  project_name    = "auth-sevice"
}
