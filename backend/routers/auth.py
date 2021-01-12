from hashlib import sha256

import jwt
from backend.database import get_db
from backend.models import Credentials, User
from backend.schemas import CredentialIn
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter()

TOKEN_SECRET = "so secret secret"


@router.post(
    "/signup",
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Login already exists"}},
)
def signup(cred: CredentialIn, db: Session = Depends(get_db)):

    db_user = User()

    hashed_password = sha256(cred.password.encode()).hexdigest()

    db_cred = Credentials(login=cred.login, password=hashed_password, user=db_user)

    db.add_all([db_user, db_cred])

    try:
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Login already exists"
        )


@router.post(
    "/auth",
    responses={status.HTTP_403_FORBIDDEN: {"detail": "Login or password invalid"}},
)
def auth(cred: CredentialIn, db: Session = Depends(get_db)):

    hashed_password = sha256(cred.password.encode()).hexdigest()

    db_cred = (
        db.query(Credentials)
        .filter(Credentials.login == cred.login)
        .filter(Credentials.password == hashed_password)
        .one_or_none()
    )

    if db_cred is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Login or password invalid"
        )

    token = jwt.encode({"login": cred.login}, TOKEN_SECRET, algorithm="HS256")

    return {"token": token}
