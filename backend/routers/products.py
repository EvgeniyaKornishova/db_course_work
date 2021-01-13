from backend.cruds import product as products_cruds
from backend.database import get_db
from backend.schemas.products import ProductsIn, ProductsUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/{shopping_list_id}")
def list(
    shopping_list_id: int,
    db: Session = Depends(get_db),
) -> list:
    products = products_cruds.list(db=db, shopping_list_id=shopping_list_id)

    return products


@router.post("/")
def create(
    product: ProductsIn,
    db: Session = Depends(get_db),
) -> None:
    products_cruds.create(product=product, db=db)


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
