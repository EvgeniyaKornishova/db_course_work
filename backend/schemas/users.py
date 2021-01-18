from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    max_stress_lvl: int
    cur_stress_lvl: int
    balance: float

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    max_stress_lvl: Optional[int] = None
    cur_stress_lvl: Optional[int] = None
    balance: Optional[float] = None


class UserStressIn(BaseModel):
    max_stress_lvl: int


class UserBalanceIn(BaseModel):
    balance: float
