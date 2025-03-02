import magic
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import Response

from .adapter import (
    adapter,
    NotFoundResponse,
    UnExpectedErrorResponse,
)
from ...shared.responses import to_openapi

r = APIRouter(prefix="/files", tags=["Files"])
IncorrectUrlResponse = HTTPException(status_code=422, detail="Incorrect url")


@r.get(
    "/view/{url:path}",
    responses={
        **to_openapi(NotFoundResponse),
        **to_openapi(UnExpectedErrorResponse),
        **to_openapi(IncorrectUrlResponse),
    },
)
async def view(url: str) -> Response:
    """
    **url** должно быть вида **profiles/dima.png** , без начального слеша в query params
    """
    if url[0] == "/":
        url = url[1:]

    fp_group = url.split("/")
    if len(fp_group) != 2:
        raise IncorrectUrlResponse
    bucket_name, file_name = fp_group[0], fp_group[1]
    resp = await adapter.get_file(bucket_name, file_name)
    return Response(
        content=resp,
        media_type=magic.from_buffer(resp, mime=True),
        # headers={"Content-Disposition": f"attachment; filename={file_name}"},
    )
