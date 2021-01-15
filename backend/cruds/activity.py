from datetime import date, datetime
from typing import Optional

from backend import models
from backend.schemas import activities as schemas
from sqlalchemy.orm import Session


def get_activity_in_schema(type: str):
    if type == "work":
        return schemas.Work
    elif type == "meeting":
        return schemas.Meeting
    elif type == "shopping":
        return schemas.Shopping
    elif type == "studying":
        return schemas.Studying
    elif type == "sport":
        return schemas.Sport
    elif type == "other":
        return schemas.OtherActivity
    else:
        return None


def get_activity_out_schema(type: str):
    if type == "work":
        return schemas.WorkOut
    elif type == "meeting":
        return schemas.MeetingOut
    elif type == "shopping":
        return schemas.ShoppingOut
    elif type == "studying":
        return schemas.StudyingOut
    elif type == "sport":
        return schemas.SportOut
    elif type == "other":
        return schemas.OtherActivityOut
    else:
        return None


def get_activity_model(type: str):
    if type == "work":
        return models.Work
    elif type == "meeting":
        return models.Meeting
    elif type == "shopping":
        return models.Shopping
    elif type == "studying":
        return models.Studying
    elif type == "sport":
        return models.Sport
    elif type == "other":
        return models.OtherActivity
    else:
        return None


def list(
    db: Session,
    user_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
) -> list:
    activities = []

    if start_time is None and end_time is None:
        activities = (
            db.query(models.Activity).filter(models.Activity.user_id == user_id).all()
        )
    elif start_time is None:
        activities = (
            db.query(models.Activity)
            .filter(models.Activity.user_id == user_id)
            .filter(models.Activity.end_time <= end_time)
            .all()
        )
    elif end_time is None:
        activities = (
            db.query(models.Activity)
            .filter(models.Activity.user_id == user_id)
            .filter(models.Activity.start_time >= start_time)
            .all()
        )
    else:  # start_time and end_time specified
        activities = (
            db.query(models.Activity)
            .filter(models.Activity.user_id == user_id)
            .filter(models.Activity.start_time >= start_time)
            .filter(models.Activity.end_time <= end_time)
            .all()
        )

    for activity in activities:
        if activity.period:
            while (
                activity.processing_date < date.today()
                or activity.processing_date <= activity.end_time.date()
            ):
                activity.processing_date += activity.period
    db.commit()

    out_activities = []

    for activity in activities:
        in_schema = get_activity_in_schema(activity.activity_type)
        out_schema = get_activity_out_schema(activity.activity_type)
        model = get_activity_model(activity.activity_type)

        activity_ext = db.query(model).filter(model.activity_id == activity.id).first()

        sch_base = schemas.ActivityOut(**activity.__dict__)
        sch_ext = in_schema(**activity_ext.__dict__)

        out_activity = out_schema(**sch_base.dict(), **sch_ext.dict())

        out_activities.append(out_activity)

    return out_activities


def create(db: Session, activity: schemas.FullActivityIn, user_id: int) -> None:
    row_activity = schemas.ActivityIn(**activity.dict())

    activity_base = models.Activity(**row_activity.dict(), user_id=user_id)

    schema = get_activity_in_schema(row_activity.activity_type)
    model = get_activity_model(row_activity.activity_type)

    if schema is None or model is None:
        raise ValueError("Unsupported action type")

    activity_ext = model(**schema(**activity.dict()).dict(), activity=activity_base)

    db.add(activity_base)
    db.add(activity_ext)
    db.commit()


def update(
    db: Session, activity: schemas.FullActivityUpdate, activity_id: int, user_id: int
) -> None:
    activity_base_update = schemas.ActivityUpdate(**activity.dict()).dict(
        exclude_none=True
    )

    if activity_base_update:
        db.query(models.Activity).filter(models.Activity.user_id == user_id).filter(
            models.Activity.id == activity_id
        ).update(activity_base_update)

    activity_type = (
        db.query(models.Activity.activity_type)
        .filter(models.Activity.user_id == user_id)
        .filter(models.Activity.id == activity_id)
        .first()
        .activity_type
    )

    schema = get_activity_in_schema(activity_type)
    model = get_activity_model(activity_type)

    if schema is None or model is None:
        raise ValueError("Unsupported action type")

    activity_ext_update = schema(**activity.dict()).dict(exclude_none=True)

    if activity_ext_update:
        db.query(model).filter(model.activity_id == activity_id).update(
            activity_ext_update
        )

    db.commit()


def delete(db: Session, activity_id: int, user_id: int) -> None:
    db.query(models.Activity).filter(models.Activity.user_id == user_id).filter(
        models.Activity.id == activity_id
    ).delete()
    db.commit()
