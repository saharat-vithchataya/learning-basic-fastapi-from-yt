from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from schemas import PostCreate, PostOut
from oauth2 import get_current_user
from database import get_db
import models

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PostOut])
async def get_posts(
    limit: int = 10,
    skip: int = 0,
    search: str | None = "",
    db: Session = Depends(get_db),
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.get("/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    entity: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_post = models.Post(
        title=entity.title,
        content=entity.content,
        published=entity.published,
        owner_id=current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
