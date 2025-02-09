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

resource "yandex_iam_service_account" "sa" {
  name = "${local.resource_prefix}-sa"
}

resource "yandex_resourcemanager_folder_iam_binding" "roles" {
  for_each = toset([
    "admin",
    "storage.admin",
    "container-registry.admin", "container-registry.images.puller",
  ])
  members = [
    "serviceAccount:${yandex_iam_service_account.sa.id}"
  ]
  role = each.key
  folder_id = var.folder_id
}

resource "yandex_iam_service_account_static_access_key" "keys" {
  service_account_id = yandex_iam_service_account.sa.id
}

output "sa_id" {
  value = yandex_iam_service_account.sa.id
}

output "sa_access_key" {
  value = "${nonsensitive(yandex_iam_service_account_static_access_key.keys.access_key)}"
}
output "sa_secret_key" {
  value = "${nonsensitive(yandex_iam_service_account_static_access_key.keys.secret_key)}"

}


locals {
  resource_prefix = "${local.project_name}"
  zone            = "ru-central1-a"
  project_name    = "auth-sevice"
}
