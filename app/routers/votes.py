from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from schemas import VoteCreate
from oauth2 import get_current_user
from database import get_db
import models

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def vote(
    vote: VoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user has already voted on post",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
