data "yandex_function" "authorization" {
  name       = "authorization"
}

# uv pip freeze > requirements.txt
# zip -r authorization.zip * -x .venv -x uv.lock -x README.md -x pyproject.toml -x -x .*
# mv authorization.zip infra/data/