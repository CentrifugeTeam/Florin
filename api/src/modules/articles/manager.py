from fastapi_sqlalchemy_toolkit import ModelManager
from ...db import Article
from sqlmodel import select
from sqlalchemy.orm import joinedload


class ArticleManager(ModelManager):
    async def paginated_list(self, session, page, limit):
        offset = (page - 1) * limit
        return await session.exec(
            select(self.model)
            .options(joinedload(Article.plant))
            .offset(offset)
            .limit(limit)
        )


article_manager = ArticleManager(Article)
