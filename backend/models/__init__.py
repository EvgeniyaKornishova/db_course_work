from backend.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "пользователь"

    id = Column("id_пользователя", Integer, primary_key=True)
    max_stress_lvl = Column("макс_допустимый_ус", Integer, default=600)
    cur_stress_lvl = Column("текущий_ус", Integer, default=0)


class Credentials(Base):
    __tablename__ = "credentials"

    user_id = Column(
        Integer, ForeignKey("пользователь.id_пользователя"), primary_key=True
    )
    login = Column(String)
    password = Column(String)

    user = relationship("User")


class Location(Base):
    __tablename__ = "локация"

    id = Column("id_локации", Integer, primary_key=True)
    name = Column("название", String)
    user_id = Column(
        "id_пользователя", Integer, ForeignKey("пользователь.id_пользователя")
    )

    user = relationship("User")
