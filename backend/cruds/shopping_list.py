from backend.models import ShoppingList
from backend.schemas.shopping_lists import ShoppingListIn
from sqlalchemy.orm import Session


def list(db: Session, user_id: int) -> list:
    shopping_lists = (
        db.query(ShoppingList).filter(ShoppingList.user_id == user_id).all()
    )

    return shopping_lists


def create(db: Session, shopping_list: ShoppingListIn, user_id: int) -> None:
    db_shopping_list = ShoppingList(**shopping_list.dict(), user_id=user_id)

    db.add(db_shopping_list)
    db.commit()


def update(
    db: Session, shopping_list: ShoppingListIn, shopping_list_id: int, user_id: int
) -> None:
    db.query(ShoppingList).filter(ShoppingList.user_id == user_id).filter(
        ShoppingList.id == shopping_list_id
    ).update({**shopping_list.dict(exclude_none=True)})
    db.commit()


def delete(db: Session, shopping_list_id: int, user_id: int) -> None:
    db.query(ShoppingList).filter(ShoppingList.user_id == user_id).filter(
        ShoppingList.id == shopping_list_id
    ).delete()
    db.commit()
