from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.models import Base
from backend.routers import auth, locations, products
from backend.routers.dependencies import get_user_id

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
app.include_router(
    locations.router,
    prefix="/locations",
    tags=["Locations"],
    dependencies=[Depends(get_user_id)],
)
app.include_router(
    products.router,
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_user_id)],
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)
