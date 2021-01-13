from backend.cruds import shopping_list as shopping_list_cruds
from backend.database import get_db
from backend.routers.dependencies import get_user_id
from backend.schemas.shopping_lists import ShoppingListIn
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def list(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)) -> list:
    shopping_lists = shopping_list_cruds.list(db=db, user_id=user_id)

    return shopping_lists


@router.post("/")
def create(
    shopping_list: ShoppingListIn,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    shopping_list_cruds.create(shopping_list=shopping_list, user_id=user_id, db=db)


@router.put(
    "/{shopping_list_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Shopping list with specified id not found"
        }
    },
)
def update(
    shopping_list_id: int,
    shopping_list: ShoppingListIn,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    try:
        shopping_list_cruds.update(
            shopping_list_id=shopping_list_id,
            shopping_list=shopping_list,
            user_id=user_id,
            db=db,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shopping list with specified id not found",
        )


@router.delete(
    "/{shopping_list_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Shopping list with specified id not found"
        }
    },
)
def delete(
    shopping_list_id: int,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    try:
        shopping_list_cruds.delete(
            db=db, shopping_list_id=shopping_list_id, user_id=user_id
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shopping list with specified id not found",
        )
