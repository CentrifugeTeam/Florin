resource "yandex_storage_bucket" "internal" {
  bucket     = "${local.resource_prefix}-internal-use-bucket"
  secret_key = yandex_iam_service_account_static_access_key.keys.secret_key
  access_key = yandex_iam_service_account_static_access_key.keys.access_key
}

resource "yandex_storage_object" "authorization" {
  bucket = yandex_storage_bucket.internal.bucket
  key    = "authorization"
  source = "${path.root}/data/authorization.zip"
}

