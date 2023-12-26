from typing import Optional

from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Article
class ArticleBase(BaseModel):
    name: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(ArticleBase):
    name: Optional[str] = None
    content: Optional[str] = None


class Article(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# Comment
class CommentBase(BaseModel):
    content: str
    article_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    content: Optional[str] = None
    article_id: Optional[int] = None


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
