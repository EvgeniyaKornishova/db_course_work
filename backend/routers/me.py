from datetime import date, datetime

from backend.cruds import activity as activitiy_cruds
from backend.cruds import user as user_cruds
from backend.routers.dependencies import get_db, get_user_id
from backend.schemas.users import UserBalanceIn, UserStressIn, UserUpdate
from backend.utils.schedule import make_plan
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/stress")
def get_stress(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> int:
    user = user_cruds.get(db=db, user_id=user_id)

    return {
        "current_stress": user.cur_stress_lvl,
        "max_stress": user.max_stress_lvl,
    }


@router.put("/stress")
def update_max_stress_lvl(
    _max_stress_lvl: UserStressIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> None:
    user_cruds.update(db=db, user=UserUpdate(**_max_stress_lvl.dict()), user_id=user_id)


@router.get("/schedule")
def generate_plan(
    sch_date: date, db: Session = Depends(get_db), user_id: int = Depends(get_user_id)
) -> None:
    if sch_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schedule can be generated only for the future days",
        )

    try:
        plan = make_plan(db=db, user_id=user_id, plan_date=sch_date)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    # get fulls
    schedule = [activitiy_cruds.get(db, user_id, id, full=True) for id in plan]

    # change time window

    for activity in schedule:
        activity.start_time = datetime.fromtimestamp(plan[activity.id].start)
        activity.end_time = datetime.fromtimestamp(plan[activity.id].end)

    return schedule


@router.get("/balance")
def get_balance(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> None:
    user = user_cruds.get(db=db, user_id=user_id)

    return {
        "balance": user.balance,
    }


@router.put("/balance")
def change_balance(
    _balance: UserBalanceIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> None:
    user_cruds.update(db=db, user=UserUpdate(**_balance.dict()), user_id=user_id)
