from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    surname: str
    max_stress_lvl: int
    cur_stress_lvl: int

    class Config:
        orm_mode = True
