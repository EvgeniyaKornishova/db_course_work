from backend.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "пользователь"

    id = Column('id_пользователя', Integer, primary_key=True)
    name = Column('имя', String)
    surname = Column('фамилия', String)
    max_stress_lvl = Column('макс_допустимый_ус', Integer)
    cur_stress_lvl = Column('текущий_ус', Integer)
