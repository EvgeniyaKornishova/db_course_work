from backend.database import get_db
from backend.models import User as model
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/users")
async def list_users(db: Session = Depends(get_db)):
    return db.query(model).all()
