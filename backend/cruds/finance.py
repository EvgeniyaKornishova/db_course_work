from datetime import date
from typing import List, Optional

from backend import models
from backend.schemas import finance as schemas
from sqlalchemy.orm import Session


def list(
    db: Session,
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[schemas.Finance]:
    queries = [models.Finance.user_id == user_id]

    if start_date:
        queries.append(models.Finance.date >= start_date)
    if end_date:
        queries.append(models.Finance.date <= end_date)

    finances = db.query(models.Finance).filter(*queries).all()

    return finances


def get(db: Session, user_id: int, finance_id: int) -> schemas.Finance:

    finance = (
        db.query(models.Finance)
        .filter(models.Finance.user_id == user_id)
        .filter(models.Finance.id == finance_id)
        .one_or_none()
    )

    return finance


def create(db: Session, user_id: int, finance: schemas.FinanceIn) -> None:
    finance = models.Finance(**finance.dict(), user_id=user_id)

    db.add(finance)
    db.commit()

    return finance.id


def update(
    db: Session, user_id: int, finance_id: int, finance: schemas.FinanceUpdate
) -> None:
    db.query(models.Finance).filter(models.Finance.user_id == user_id).filter(
        models.Finance.id == finance_id
    ).update(finance.dict(exclude_none=True))

    db.commit()


def delete(db: Session, user_id: int, finance_id: int) -> None:
    db.query(models.Finance).filter(models.Finance.user_id == user_id).filter(
        models.Finance.id == finance_id
    ).delete()

    db.commit()
