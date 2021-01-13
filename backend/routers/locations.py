from backend.cruds import location as location_cruds
from backend.database import get_db
from backend.routers.dependencies import get_user_id
from backend.schemas.location import LocationIn
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
def list(db: Session = Depends(get_db), user_id: int = Depends(get_user_id)) -> list:
    locations = location_cruds.list(db=db, user_id=user_id)

    return locations


@router.post("/")
def create(
    _name: LocationIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
) -> None:
    name = _name.name
    location_cruds.create(name=name, db=db, user_id=user_id)


@router.put(
    "/{location_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Location with specified id not found"
        }
    },
)
def update(
    location_id: int,
    _name: LocationIn,
    user_id: int = Depends(get_user_id),
    db: Session = Depends(get_db),
) -> None:
    name = _name.name
    try:
        location_cruds.update(
            location_id=location_id, user_id=user_id, name=name, db=db
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location with specified id not found",
        )


@router.delete(
    "/{location_id}",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Location with specified id not found"
        }
    },
)
def delete(location_id: int, db: Session = Depends(get_db)) -> None:
    try:
        location_cruds.delete(db=db, location_id=location_id)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location with specified id not found",
        )
