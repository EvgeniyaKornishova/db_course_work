from pydantic import BaseModel


class User(BaseModel):
    id: int
    max_stress_lvl: int
    cur_stress_lvl: int

    class Config:
        orm_mode = True
