from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class ProductsOut(BaseModel):
    id: int
    name: str
    price: float
    amount: int
    deadline: datetime
    approved: str
    shopping_list_id: int

    @validator("approved")
    def approved_enum(cls, v):
        if v not in ["подтвержден", "не подтвержден"]:
            raise ValueError("Format must be 'подтвержден' or 'не подтвержден'")
        return v


class ProductsIn(BaseModel):
    name: str
    price: float
    amount: int
    deadline: datetime
    shopping_list_id: int


class ProductsUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    amount: Optional[int] = None
    deadline: Optional[datetime] = None
    approved: Optional[str] = None
    shopping_list_id: Optional[int] = None

    @validator("approved")
    def approved_enum(cls, v):
        if v and v not in ["подтвержден", "не подтвержден"]:
            raise ValueError("Format must be 'подтвержден' or 'не подтвержден'")
        return v
