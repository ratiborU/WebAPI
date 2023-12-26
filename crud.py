from sqlalchemy.orm import Session

import schemas
from models import Article, Comment


# Article
def create_article(db: Session, schema: schemas.ArticleCreate):
    db_article = Article(**schema.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()


def get_article(db: Session, article_id: int):
    return db.query(Article).filter_by(id=article_id).first()


def update_article(db: Session, article_id: int, article_data: schemas.ArticleUpdate):
    db_article = db.query(Article).filter_by(id=article_id).first()
    article_data = article_data if isinstance(article_data, dict) else article_data.model_dump()

    if db_article:
        for key, value in article_data.items():
            if hasattr(db_article, key):
                setattr(db_article, key, value)

        db.commit()
        db.refresh(db_article)

    return db_article


def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter_by(id=article_id).first()
    if db_article:
        db.delete(db_article)
        db.commit()
        return True
    return False


# Comment
def create_comment(db: Session, schema: schemas.CommentCreate):
    db_comment = Comment(**schema.model_dump())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Comment).offset(skip).limit(limit).all()


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter_by(id=comment_id).first()


def update_comment(db: Session, comment_id: int, comment_data: schemas.CommentUpdate):
    db_comment = db.query(Comment).filter_by(id=comment_id).first()
    comment_data = comment_data if isinstance(comment_data, dict) else comment_data.model_dump()
    if db_comment:
        for key, value in comment_data.items():
            if hasattr(db_comment, key):
                setattr(db_comment, key, value)

        db.commit()
        db.refresh(db_comment)
        return db_comment
    return None


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter_by(id=comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return True
    return False

