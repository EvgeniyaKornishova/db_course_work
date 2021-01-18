from datetime import date

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
        if v and v not in ["доход", "расход"]:
            raise ValueError("Format must be 'доход' or 'расход'")
        return v


class FinanceIn(BaseModel):
    type: str
    cost: float
    item: str
    date: date

    @validator("type")
    def type_enum(cls, v):
        if v and v not in ["доход", "расход"]:
            raise ValueError("Format must be 'доход' or 'расход'")
        return v
