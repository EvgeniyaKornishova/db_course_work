import jwt
from backend.database import get_db
from backend.models import Credentials
from backend.routers.auth import TOKEN_SECRET
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session


def get_token(authorization: str = Header(None)) -> dict:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required"
        )

    schema, _, token = authorization.partition(" ")

    if schema != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )

    try:
        data = jwt.decode(token, TOKEN_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )

    return data


def get_user_id(_login: str = Depends(get_token), db: Session = Depends(get_db)) -> int:
    login = _login["login"]

    response = (
        db.query(Credentials.user_id).filter(Credentials.login == login).one_or_none()
    )

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )

    return response.user_id
