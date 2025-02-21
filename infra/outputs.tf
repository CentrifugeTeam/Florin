output "sa_id" {
  value = yandex_iam_service_account.sa.id
}

output "access_secret_key" {
  value = "${nonsensitive(yandex_iam_service_account_static_access_key.keys.access_key)}"
}
output "secret_key" {
  value = "${nonsensitive(yandex_iam_service_account_static_access_key.keys.secret_key)}"
}

output "ydb" {
  value = yandex_ydb_database_serverless.ydb.database_path
}

output "ydb2" {
  value = yandex_ydb_database_serverless.ydb.ydb_api_endpoint
}

output "internal-bucket" {
  value = yandex_storage_bucket.internal.bucket
}