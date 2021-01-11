from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.database import SessionLocal, engine
from backend.models import Base
from backend.models import User as model

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
async def list_users(db: Session = Depends(get_db)):
    return db.query(model).all()


@app.get("/")
async def root():
    return {"message": "Hello World"}
