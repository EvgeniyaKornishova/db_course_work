from backend.cruds import product as products_cruds
from backend.cruds import user as user_cruds
from backend.database import get_db
from backend.routers.dependencies import get_user_id
from backend.schemas.products import ProductsIn, ProductsOut, ProductsUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{shopping_list_id}")
def list(
    shopping_list_id: int,
    db: Session = Depends(get_db),
) -> list:
    products = products_cruds.list(db=db, shopping_list_id=shopping_list_id)

    products_out = [ProductsOut(product.__dict__) for product in products]

    return products_out


@router.post("/")
def create(
    product: ProductsIn,
    db: Session = Depends(get_db),
):
    product_id = products_cruds.create(product=product, db=db)

    return {"id": product_id}


@router.put(
    "/{product_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Product with specified id not found"
        }
    },
)
def update(
    product_id: int,
    product: ProductsUpdate,
    db: Session = Depends(get_db),
) -> None:
    try:
        products_cruds.update(product_id=product_id, product=product, db=db)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with specified id not found",
        )


@router.delete(
    "/{product_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Product with specified id not found"
        }
    },
)
def delete(product_id: int, db: Session = Depends(get_db)) -> None:
    try:
        products_cruds.delete(db=db, product_id=product_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with specified id not found",
        )


@router.post("/{product_id}/complete")
def complete(
    product_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_user_id)
) -> None:
    products_cruds.update(
        db=db, product_id=product_id, product=ProductsUpdate(approved="подтвержден")
    )

    product = products_cruds.get(db=db, product_id=product_id)

    # update user's balance
    user = user_cruds.get(db, user_id)
    balance = user.balance - product.price * product.amount

    user_cruds.update(db, UserUpdate(balance=balance), user_id=user_id)
