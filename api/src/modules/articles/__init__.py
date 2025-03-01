from ...deps import GetSession
from fastapi_libkit.responses import ErrorModel, not_found_response, no_content_response
from sqlalchemy.orm import joinedload
from uuid import UUID
from fastapi import APIRouter, Query, Body, Response
from typing import Annotated
from .manager import article_manager
from .schema import ArticleRead
from ...db import Article


r = APIRouter(prefix="/articles", tags=["Articles for house plants"])


@r.get("", response_model=list[ArticleRead])
async def articles(
    session: GetSession,
    limit: Annotated[int, Query(gt=0)] = 10,
    page: Annotated[int, Query(gt=0)] = 1,
):
    return await article_manager.paginated_list(session, page, limit)


@r.get(
    "/{id}",
    response_model=ArticleRead,
    responses={404: {"model": ErrorModel, "detail": "Not found"}},
)
async def article(session: GetSession, id: UUID):
    return await article_manager.get_or_404(
        session, id=id, options=joinedload(Article.plant)
    )
