from pydantic import BaseModel


class ShoppingListIn(BaseModel):
    name: str
