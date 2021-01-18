from datetime import date
from typing import List, Optional

from backend.cruds import finance as finance_cruds
from backend.cruds import user as user_cruds
from backend.routers.dependencies import get_db, get_user_id
from backend.schemas.finance import Finance, FinanceIn
from backend.schemas.users import UserUpdate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def list(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> List[Finance]:
    finances = finance_cruds.list(
        db=db, user_id=user_id, start_date=start_date, end_date=end_date
    )

    return finances


@router.post("/")
def create(
    finance: FinanceIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> List[Finance]:
    id = finance_cruds.create(db=db, user_id=user_id, finance=finance)

    # update user's balance
    user = user_cruds.get(db, user_id)
    balance = user.balance

    if finance.type == "доход":
        balance += finance.cost
    else:
        balance -= finance.cost

    user_cruds.update(db, UserUpdate(balance=balance), user_id=user_id)

    return {"id": id}
