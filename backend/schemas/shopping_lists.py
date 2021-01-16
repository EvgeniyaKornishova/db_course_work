from typing import List

from backend.schemas.products import ProductsOut
from pydantic import BaseModel


class ShoppingListIn(BaseModel):
    name: str


class ShoppingListOut(BaseModel):
    id: int
    name: str
    products: List[ProductsOut] = []
