
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
