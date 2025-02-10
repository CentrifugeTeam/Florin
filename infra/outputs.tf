output "sa_id" {
  value = yandex_iam_service_account.sa.id
}

output "sa_access_key" {
  value = "${nonsensitive(yandex_iam_service_account_static_access_key.keys.access_key)}"
}
output "sa_secret_key" {
  value = "${nonsensitive(yandex_iam_service_account_static_access_key.keys.secret_key)}"
}


output "internal-bucket" {
  value = yandex_storage_bucket.internal.bucket
}