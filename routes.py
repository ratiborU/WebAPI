from typing import List

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

import schemas
from database import get_db
from sqlalchemy.orm import Session
from crud import (
    create_article, get_articles, get_article, update_article, delete_article,
    create_comment, get_comment, get_comments, update_comment, delete_comment
)

router_websocket = APIRouter()
router_articles = APIRouter(prefix='/articles', tags=['article'])
router_comments = APIRouter(prefix='/comments', tags=['comment'])


# WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


async def notify_clients(message: str):
    for connection in manager.active_connections:
        await connection.send_text(message)


@router_websocket.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Пользователь #{client_id} присоединился к чату")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"Ваше сообщение: {data}", websocket)
            await manager.broadcast(f"Пользователь #{client_id} написл(а): {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь #{client_id} покинул(а) чат")


# # Категории
# @router_categories.post("/", response_model=schemas.Category)
# async def create_category_route(category_data: schemas.CategoryCreate, db: Session = Depends(get_db)):
#     category = create_category(db, category_data)
#     await notify_clients(f"Category added: {category.name}")
#     return category
#
#
# @router_categories.get("/", response_model=List[schemas.Category])
# async def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     categories = get_categories(db, skip=skip, limit=limit)
#     return categories
#
#
# @router_categories.get("/{category_id}", response_model=schemas.Category)
# async def read_category(category_id: int, db: Session = Depends(get_db)):
#     category = get_category(db, category_id)
#     return category
#
#
# @router_categories.patch("/{category_id}", response_model=schemas.Category)
# async def update_category_route(category_id: int, category_data: schemas.CategoryUpdate, db: Session = Depends(get_db)):
#     updated_category = update_category(db, category_id, category_data)
#     if updated_category:
#         await notify_clients(f"Category updated: {updated_category.name}")
#         return updated_category
#     return {"message": "Category not found"}
#
#
# @router_categories.delete("/{category_id}")
# async def delete_category_route(category_id: int, db: Session = Depends(get_db)):
#     deleted = delete_category(db, category_id)
#     if deleted:
#         await notify_clients(f"Category deleted: ID {category_id}")
#         return {"message": "Category deleted"}
#     return {"message": "Category not found"}
#
#
# # Товары
# @router_items.post("/", response_model=schemas.Item)
# async def create_item_route(schema: schemas.ItemCreate, db: Session = Depends(get_db)):
#     item = create_item(db, schema)
#     await notify_clients(f"Item added: {item.name}")
#     return item
#
#
# @router_items.get("/", response_model=List[schemas.Item])
# async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     items = get_items(db, skip=skip, limit=limit)
#     return items
#
#
# @router_items.get("/{item_id}", response_model=schemas.Item)
# async def read_item(item_id: int, db: Session = Depends(get_db)):
#     item = get_item(db, item_id)
#     return item
#
#
# @router_items.patch("/{item_id}")
# async def update_item_route(item_id: int, schema: schemas.ItemUpdate, db: Session = Depends(get_db)):
#     updated_item = update_item(db, item_id, schema)
#     if updated_item:
#         await notify_clients(f"Item updated: {updated_item.name}")
#         return updated_item
#     return {"message": "Item not found"}
#
#
# @router_items.delete("/{item_id}")
# async def delete_item_route(item_id: int, db: Session = Depends(get_db)):
#     deleted = delete_item(db, item_id)
#     if deleted:
#         await notify_clients(f"Item deleted: ID {item_id}")
#         return {"message": "Item deleted"}
#     return {"message": "Item not found"}


# Статьи
@router_articles.post("/", response_model=schemas.Article)
async def create_article_route(article_data: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = create_article(db, article_data)
    await notify_clients(f"Article added: {article.name}")
    return article


@router_articles.get("/", response_model=List[schemas.Article])
async def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    articles = get_articles(db, skip=skip, limit=limit)
    return articles


@router_articles.get("/{article_id}", response_model=schemas.Article)
async def read_article(article_id: int, db: Session = Depends(get_db)):
    article = get_article(db, article_id)
    return article


@router_articles.patch("/{article_id}", response_model=schemas.Article)
async def update_article_route(article_id: int, article_data: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    updated_article = update_article(db, article_id, article_data)
    if updated_article:
        await notify_clients(f"Article updated: {updated_article.name}")
        await notify_clients(f"Article updated: {updated_article.content}")
        return updated_article
    return {"message": "Article not found"}


@router_articles.delete("/{article_id}")
async def delete_article_route(article_id: int, db: Session = Depends(get_db)):
    deleted = delete_article(db, article_id)
    if deleted:
        await notify_clients(f"Article deleted: ID {article_id}")
        return {"message": "Article deleted"}
    return {"message": "Article not found"}


# Комментарии
@router_comments.post("/", response_model=schemas.Comment)
async def create_comment_route(schema: schemas.CommentCreate, db: Session = Depends(get_db)):
    comment = create_comment(db, schema)
    await notify_clients(f"Comment added: {comment.content}")
    return comment


@router_comments.get("/", response_model=List[schemas.Comment])
async def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comments = get_comments(db, skip=skip, limit=limit)
    return comments


@router_comments.get("/{comment_id}", response_model=schemas.Comment)
async def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = get_comment(db, comment_id)
    return comment


@router_comments.patch("/{comment_id}")
async def update_comment_route(comment_id: int, schema: schemas.CommentUpdate, db: Session = Depends(get_db)):
    updated_comment = update_comment(db, comment_id, schema)
    if updated_comment:
        await notify_clients(f"Comment updated: {updated_comment.content}")
        return updated_comment
    return {"message": "Comment not found"}


@router_comments.delete("/{comment_id}")
async def delete_comment_route(comment_id: int, db: Session = Depends(get_db)):
    deleted = delete_comment(db, comment_id)
    if deleted:
        await notify_clients(f"Comment deleted: ID {comment_id}")
        return {"message": "Comment deleted"}
    return {"message": "Comment not found"}

