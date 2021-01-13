from fastapi import Depends, FastAPI

from backend.database import engine
from backend.models import Base
from backend.routers import auth, locations
from backend.routers.dependencies import get_user_id

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
app.include_router(
    locations.router,
    prefix="/locations",
    tags=["Locations"],
    dependencies=[Depends(get_user_id)],
)

Base.metadata.create_all(bind=engine)
