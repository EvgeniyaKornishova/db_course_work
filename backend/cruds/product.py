from backend.models import Products
from backend.schemas.products import ProductsIn, ProductsUpdate
from sqlalchemy.orm import Session


def list(db: Session, shopping_list_id: int) -> list:
    products = (
        db.query(Products).filter(Products.shopping_list_id == shopping_list_id).all()
    )

    return products


def create(db: Session, product: ProductsIn) -> None:
    db_product = Products(**product.dict())

    db.add(db_product)
    db.commit()


def update(db: Session, product: ProductsUpdate, product_id: int) -> None:
    # TODO: Add check on deadline

    db.query(Products).filter(Products.id == product_id).update(
        {**product.dict(exclude_none=True)}
    )
    db.commit()


def delete(db: Session, product_id: int) -> None:
    # TODO: Add check on empty shopping list

    db.query(Products).filter(Products.id == product_id).delete()
    db.commit()
