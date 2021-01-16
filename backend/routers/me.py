from datetime import date

from backend.cruds import activity as activitiy_cruds
from backend.cruds import user as user_cruds
from backend.routers.dependencies import get_db, get_user_id
from backend.schemas.users import UserStressIn, UserUpdate
from fastapi import APIRouter, Depends
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


# @router.get("/plan")
# def generate_plan(
#     db: Session = Depends(get_db), user_id: int = Depends(get_user_id)
# ) -> None:
#     # TODO: make work with date
#     activitiy_cruds.make_plan(
#         db=db, user_id=user_id, plan_date=date(year=2021, month=1, day=30)
#     )
