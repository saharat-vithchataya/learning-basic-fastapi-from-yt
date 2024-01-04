from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from database import get_db
from oauth2 import get_current_user
from schemas import PersonalInformation, PersonalInformationOut
import models

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def create_new_personal_information(
    psi: PersonalInformation,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_psi = models.PersonalInformation(
        firstname=psi.firstname,
        lastname=psi.lastname,
        phone=psi.phone,
        date_of_birth=psi.date_of_birth,
        address=psi.date_of_birth,
        user_id=current_user.id,
    )
    db.add(new_psi)
    db.commit()
    db.refresh(new_psi)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PersonalInformationOut,
)
async def get_personal_infomation(
    id: int,
    db: Session = Depends(get_db),
    # current_user=Depends(get_current_user),
):
    psi = (
        db.query(models.PersonalInformation)
        .filter(models.PersonalInformation.id == id)
        .first()
    )

    if not psi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return psi
