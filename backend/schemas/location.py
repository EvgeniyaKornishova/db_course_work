from pydantic import BaseModel


class LocationIn(BaseModel):
    name: str
