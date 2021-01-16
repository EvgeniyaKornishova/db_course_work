from datetime import date, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, validator


class ActivityIn(BaseModel):
    start_time: datetime
    end_time: datetime
    processing_date: date
    duration: timedelta
    period: Optional[timedelta] = None
    format: str
    activity_type: str
    stress_points: int
    location_id: Optional[int] = None

    @validator("format")
    def format_enum(cls, v):
        if v not in ["очный", "дистанционный"]:
            raise ValueError("Format must be 'очный' or 'дистанционный'")
        return v


class ActivityUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    period: Optional[timedelta] = None
    format: Optional[str] = None
    stress_points: Optional[int] = None
    completed: Optional[str] = None
    location_id: Optional[int] = None

    @validator("format")
    def format_enum(cls, v):
        if v and v not in ["очный", "дистанционный"]:
            raise ValueError("Format must be 'очный' or 'дистанционный'")
        return v

    @validator("completed")
    def completed_enum(cls, v):
        if v and v not in ["выполнено", "не выполнено"]:
            raise ValueError("Format must be 'выполнено' or 'не выполнено'")
        return v


class Shopping(BaseModel):
    shopping_list_id: Optional[int] = None


class Studying(BaseModel):
    room: Optional[str] = None
    teacher: Optional[str] = None
    type: Optional[str] = None


class Sport(BaseModel):
    type: Optional[str] = None


class Work(BaseModel):
    pass


class OtherActivity(BaseModel):
    description: Optional[str] = None


class Meeting(BaseModel):
    pass


class FullActivityIn(
    ActivityIn, Shopping, Studying, Sport, Work, OtherActivity, Meeting
):
    pass


class FullActivityUpdate(
    ActivityUpdate, Shopping, Studying, Sport, Work, OtherActivity, Meeting
):
    pass


class ActivityOut(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    processing_date: date
    duration: timedelta
    period: Optional[timedelta] = None
    format: str
    activity_type: str
    stress_points: int
    location_id: Optional[int] = None
    completed: str

    class Config:
        orm_mode = True


class ShoppingOut(ActivityOut):
    shopping_list_id: Optional[int] = None


class StudyingOut(ActivityOut):
    room: Optional[str] = None
    teacher: Optional[str] = None
    type: Optional[str] = None


class SportOut(ActivityOut):
    type: Optional[str] = None


class WorkOut(ActivityOut):
    pass


class OtherActivityOut(ActivityOut):
    description: Optional[str] = None


class MeetingOut(ActivityOut):
    pass


class PlanBase(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    duration: timedelta
    format: str
    activity_type: str
    stress_points: int
    location_id: Optional[int] = None
    completed: str


class Plan(PlanBase, Shopping, Studying, Sport, Work, OtherActivity, Meeting):
    pass
