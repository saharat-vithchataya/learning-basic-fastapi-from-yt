from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import UserCreate, UserOut, TokenData
from hashing import hash
from oauth2 import get_current_user
import models

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(entity: UserCreate, db: Session = Depends(get_db)):
    exists_email = (
        db.query(models.User).filter(models.User.email == entity.email).first()
    )

    if exists_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The email is already exists",
        )
    try:
        entity.password = hash(entity.password)
        new_user = models.User(email=entity.email, hashed_password=entity.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected Error"
        )


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_profile(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return user
