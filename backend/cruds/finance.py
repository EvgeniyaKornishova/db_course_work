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
        queries.append(models.Finance.date > start_date)
    if end_date:
        queries.append(models.Finance.date < end_date)

    finances = db.query(models.Finance).filter(*queries).all()

    return finances


def create(db: Session, user_id: int, finance: schemas.FinanceIn) -> None:
    finance = models.Finance(**finance.dict(), user_id=user_id)

    db.add(finance)
    db.commit()

    return finance.id
