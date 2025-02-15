
resource "yandex_iam_service_account" "sa" {
  name = "${local.resource_prefix}-sa"
}

resource "yandex_resourcemanager_folder_iam_binding" "roles" {
  for_each = toset([
     "container-registry.images.puller", "container-registry.images.pusher",
    "serverless.containers.invoker", "serverless-containers.editor", "serverless.functions.invoker",
    "iam.serviceAccounts.user",
    "ydb.admin", "ymq.admin",
    "admin",
    "storage.admin",
    "container-registry.admin",
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
