from backend import models
from backend.schemas import users as schemas
from sqlalchemy.orm import Session


def get(db: Session, user_id: int) -> schemas.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()

    return user


def update(db: Session, user: schemas.UserUpdate, user_id: int) -> None:
    db.query(models.User).filter(models.User.id == user_id).update(
        user.dict(exclude_none=True)
    )

    db.commit()
