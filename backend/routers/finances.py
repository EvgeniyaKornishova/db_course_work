from datetime import date
from typing import List, Optional

from backend.cruds import finance as finance_cruds
from backend.cruds import user as user_cruds
from backend.routers.dependencies import get_db, get_user_id
from backend.schemas.finance import Finance, FinanceIn, FinanceUpdate
from backend.schemas.users import UserUpdate
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
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
    if finance.date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date must be today or earlier",
        )

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


@router.put("/{finance_id}")
def update(
    finance: FinanceUpdate,
    finance_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> List[Finance]:
    old_finance = finance_cruds.get(db, user_id, finance_id)

    old_type = old_finance.type == "доход"
    old_cost = old_finance.cost

    finance_cruds.update(db, user_id, finance_id, finance)

    new_finance = finance_cruds.get(db, user_id, finance_id)

    new_type = new_finance.type == "доход"
    new_cost = new_finance.cost

    financial_diff = new_cost * (1 if new_type else -1) - old_cost * (
        1 if old_type else -1
    )

    # update user's balance
    user = user_cruds.get(db, user_id)
    balance = user.balance

    balance += financial_diff

    user_cruds.update(db, UserUpdate(balance=balance), user_id=user_id)


@router.delete("/{finance_id}")
def delete(
    finance_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> None:
    finance = finance_cruds.get(db, user_id, finance_id)

    # update user's balance
    user = user_cruds.get(db, user_id)
    balance = user.balance

    type = finance.type == "доход"
    cost = finance.cost

    financial_diff = cost * (1 if type else -1)

    balance -= financial_diff

    user_cruds.update(db, UserUpdate(balance=balance), user_id=user_id)

    finance_cruds.delete(db, user_id, finance_id)
