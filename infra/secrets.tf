
resource "yandex_lockbox_secret" "secret" {
  name = "secret"
}


resource "yandex_lockbox_secret_version" "secret" {
  secret_id = yandex_lockbox_secret.secret.id
  entries {
    key = "OAUTH_KEY"
    text_value = var.oauth_key
  }
  entries {
    key = "DOCUMENT_API_ENDPOINT"
    text_value = yandex_ydb_database_serverless.ydb.ydb_api_endpoint
  }

  entries {
    key = "DOCUMENT_DATABASE_PATH"
    text_value = yandex_ydb_database_serverless.ydb.database_path
  }

  entries {
    key = "AWS_ACCESS_KEY_ID"
    text_value = yandex_iam_service_account_static_access_key.keys.access_key
  }

  entries {
    key = "AWS_SECRET_ACCESS_KEY"
    text_value = yandex_iam_service_account_static_access_key.keys.secret_key
  }

  entries {
    key = "JWT_PRIVATE_KEY"
    text_value = var.jwt_private_key
  }
}