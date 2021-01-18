from datetime import date
from typing import Optional

from pydantic import BaseModel, validator


class Finance(BaseModel):
    id: int
    type: str
    cost: float
    item: str
    date: date
    user_id: int

    @validator("type")
    def type_enum(cls, v):
        if v not in ["доход", "расход"]:
            raise ValueError("Format must be 'доход' or 'расход'")
        return v


class FinanceIn(BaseModel):
    type: str
    cost: float
    item: str
    date: date

    @validator("type")
    def type_enum(cls, v):
        if v not in ["доход", "расход"]:
            raise ValueError("Type must be 'доход' or 'расход'")
        return v


class FinanceUpdate(BaseModel):
    type: Optional[str] = None
    cost: Optional[float] = None
    item: Optional[str] = None
    date: Optional[date] = None

    class Config:
        arbitrary_types_allowed = True

    @validator("type")
    def type_enum(cls, v):
        if v and v not in ["доход", "расход"]:
            raise ValueError("Type must be 'доход' or 'расход'")
        return v
