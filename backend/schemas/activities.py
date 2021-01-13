from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class ActivityIn(BaseModel):
    start_time: datetime
    end_time: datetime
    duration: timedelta
    period: Optional[timedelta] = None
    format: str
    stress_points: int
    location_id: Optional[int] = None


class ActivityUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[timedelta] = None
    period: Optional[timedelta] = None
    format: Optional[str] = None
    stress_points: Optional[int] = None
    completed: Optional[str] = None
    location_id: Optional[int] = None
