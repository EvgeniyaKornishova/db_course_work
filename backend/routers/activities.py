from datetime import datetime
from typing import Optional

from backend.cruds import activity as activity_cruds
from backend.cruds import user as user_cruds
from backend.database import get_db
from backend.routers.dependencies import get_user_id
from backend.schemas.activities import (
    ActivityComplition,
    ActivityUpdate,
    FullActivityIn,
    FullActivityUpdate,
)
from backend.schemas.users import UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> list:
    activities = activity_cruds.list(
        db=db, user_id=user_id, start_time=start_time, end_time=end_time
    )

    return activities


@router.post("/")
def create(
    activity: FullActivityIn,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    activity_cruds.create(activity=activity, user_id=user_id, db=db)


@router.put(
    "/{activity_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Activity with specified id not found"
        }
    },
)
def update(
    activity_id: int,
    activity: FullActivityUpdate,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    try:
        activity_cruds.update(
            activity_id=activity_id,
            activity=activity,
            user_id=user_id,
            db=db,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with specified id not found",
        )


@router.delete(
    "/{activity_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Activity with specified id not found"
        }
    },
)
def delete(
    activity_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    try:
        activity_cruds.delete(db=db, activity_id=activity_id, user_id=user_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with specified id not found",
        )


@router.post(
    "/{activity_id}/complete",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Activity with specified id not found"
        }
    },
)
def complete_task(
    activity_id: int,
    _completed: ActivityComplition,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    completed = _completed.completed

    activity = activity_cruds.get(db=db, user_id=user_id, activity_id=activity_id)

    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with specified id not found",
        )

    if completed:
        if activity.completed == "выполнено":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity already completed",
            )
    else:
        if activity.completed == "не выполнено":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Activity haven't completed yet",
            )

    completed_text = "выполнено" if completed else "не выполнено"

    activity_cruds.update(
        activity_id=activity_id,
        activity=ActivityUpdate(completed=completed_text),
        user_id=user_id,
        db=db,
    )

    activity = activity_cruds.get(db=db, user_id=user_id, activity_id=activity_id)

    user = user_cruds.get(db=db, user_id=user_id)

    new_stress = user.cur_stress_lvl
    if completed:
        new_stress += activity.stress_points
    else:
        new_stress -= activity.stress_points

    user_cruds.update(
        db=db, user=UserUpdate(cur_stress_lvl=new_stress), user_id=user_id
    )

    return {"cur_stress_lvl": new_stress}
