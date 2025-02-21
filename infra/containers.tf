resource "yandex_container_registry" "registry" {
  folder_id = var.folder_id
  name = "${local.resource_prefix}-registry"

}