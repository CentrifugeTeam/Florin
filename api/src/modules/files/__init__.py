import magic
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import Response

from .adapter import adapter

r = APIRouter(prefix="/files", tags=["Files"])


@r.get("/{url:path}", deprecated=True)
async def download(url: str) -> Response:
    fp_group = url.split("/")
    if len(fp_group) != 2:
        raise HTTPException(status_code=400)
    bucket_name, file_name = fp_group[0], fp_group[1]
    resp = adapter.get_file(bucket_name, file_name)
    return Response(
        content=resp,
        media_type=magic.from_buffer(resp, mime=True),
        headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
