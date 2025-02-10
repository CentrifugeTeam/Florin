resource "yandex_function" "authorization" {
  entrypoint = "main.handler"
  memory     = 128
  name       = "authorization"
  runtime    = "python312"
  user_hash  = "${filemd5(yandex_storage_object.authorization.source)}"

  package {
    bucket_name = yandex_storage_object.authorization.bucket
    object_name = yandex_storage_object.authorization.key
  }
}
# uv pip freeze > requirements.txt
# zip -r authorization.zip * -x .venv -x uv.lock -x README.md -x pyproject.toml -x -x .*