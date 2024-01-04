from jose import jwt, JWTError
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from schemas import TokenData
from database import get_db
from config import settings
import models

oauth2_scheme = OAuth2PasswordBearer("api/auth/login")

SECRET_KEY = settings.secret_key
ALGORITHMS = settings.algorithms
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minues


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHMS)

    return access_token


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)
        id: int = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
        return token_data

    except JWTError:
        raise credential_exception


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token=token, credential_exception=credential_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
