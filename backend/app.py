from fastapi import Depends, FastAPI

from backend.database import engine
from backend.models import Base
from backend.routers import auth, users
from backend.routers.dependencies import get_user_id

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
app.include_router(users.router, tags=["Users"], dependencies=[Depends(get_user_id)])

Base.metadata.create_all(bind=engine)
