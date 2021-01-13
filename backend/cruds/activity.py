from datetime import datetime
from typing import Optional

from backend.models import Activity
from backend.schemas.activities import ActivityIn, ActivityUpdate
from sqlalchemy.orm import Session


def list(
    db: Session,
    user_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> list:
    activities = []

    if start_time is None and end_time is None:
        activities = db.query(Activity).filter(Activity.user_id == user_id).all()
    elif start_time is None:
        activities = (
            db.query(Activity)
            .filter(Activity.user_id == user_id)
            .filter(Activity.end_time <= end_time)
            .all()
        )
    elif end_time is None:
        activities = (
            db.query(Activity)
            .filter(Activity.user_id == user_id)
            .filter(Activity.start_time >= start_time)
            .all()
        )
    else:  # start_time and end_time specified
        activities = (
            db.query(Activity)
            .filter(Activity.user_id == user_id)
            .filter(Activity.start_time >= start_time)
            .filter(Activity.end_time <= end_time)
            .all()
        )

    return activities


def create(db: Session, activity: ActivityIn, user_id: int) -> None:
    activity = Activity(**activity.dict(), user_id=user_id)

    db.add(activity)
    db.commit()


def update(
    db: Session, activity: ActivityUpdate, activity_id: int, user_id: int
) -> None:
    # TODO: Add check on expired

    db.query(Activity).filter(Activity.user_id == user_id).filter(
        Activity.id == activity_id
    ).update({**activity.dict(exclude_none=True)})
    db.commit()


def delete(db: Session, activity_id: int, user_id: int) -> None:
    db.query(Activity).filter(Activity.user_id == user_id).filter(
        Activity.id == activity_id
    ).delete()
    db.commit()
