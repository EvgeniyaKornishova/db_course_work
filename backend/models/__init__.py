from backend.database import Base
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Interval,
    String,
)
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "пользователь"

    id = Column("id_пользователя", Integer, primary_key=True)
    max_stress_lvl = Column("макс_допустимый_ус", Integer, default=600)
    cur_stress_lvl = Column("текущий_ус", Integer, default=0)
    balance = Column("текущий_баланс", Float, default=0)

    activities = relationship("Activity", back_populates="user")


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


class Products(Base):
    __tablename__ = "товар"
    id = Column("id_товара", Integer, primary_key=True)
    name = Column("наименование", String)
    price = Column("стоимость", Float)
    amount = Column("количество", Integer)
    deadline = Column("срочность_покупки", Date)
    approved = Column("подтверждение", String, default="не подтвержден")
    shopping_list_id = Column("id_списка_покупок", Integer)


class ShoppingList(Base):
    __tablename__ = "список_покупок"
    id = Column("id_списка_покупок", Integer, primary_key=True)
    name = Column("название", String)
    user_id = Column(
        "id_пользователя", Integer, ForeignKey("пользователь.id_пользователя")
    )

    shopping = relationship("Shopping", back_populates="shopping_list")


class Activity(Base):
    __tablename__ = "активность"
    id = Column("id_активности", Integer, primary_key=True)
    start_time = Column("допустимое_время_начала", DateTime)
    end_time = Column("допустимое_время_конца", DateTime)
    duration = Column("продолжительность", Interval)
    period = Column("периодичность", Interval, nullable=True)
    format = Column("формат", String)
    stress_points = Column("влияние_на_уровень_стресса", Integer)
    completed = Column("готовность", String, default="не выполнено")
    processing_date = Column("дата_выполнения", Date)
    activity_type = Column("тип", String)
    location_id = Column(
        "id_локации", Integer, ForeignKey("локация.id_локации"), nullable=True
    )
    user_id = Column(
        "id_пользователя", Integer, ForeignKey("пользователь.id_пользователя")
    )
    user = relationship("User", back_populates="activities")


class Shopping(Base):
    __tablename__ = "поход_в_магазин"

    id = Column("id_похода_в_магазин", Integer, primary_key=True)
    shopping_list_id = Column(
        "id_списка_покупок",
        Integer,
        ForeignKey("список_покупок.id_списка_покупок"),
        nullable=True,
    )

    shopping_list = relationship("ShoppingList", back_populates="shopping")

    activity_id = Column(
        "id_активности", Integer, ForeignKey("активность.id_активности")
    )

    activity = relationship("Activity")


class Studying(Base):
    __tablename__ = "учебное_занятие"

    id = Column("id_учебного_занятия", Integer, primary_key=True)
    room = Column("аудитория", String)
    teacher = Column("преподаватель", String)
    type = Column("тип", String)

    activity_id = Column(
        "id_активности", Integer, ForeignKey("активность.id_активности")
    )

    activity = relationship("Activity")


class Sport(Base):
    __tablename__ = "спортивное_занятие"

    id = Column("id_спортивного_занятия", Integer, primary_key=True)
    type = Column("вид_занятия", String)

    activity_id = Column(
        "id_активности", Integer, ForeignKey("активность.id_активности")
    )

    activity = relationship("Activity")


class Work(Base):
    __tablename__ = "рабочая_смена"

    id = Column("id_рабочей_смены", Integer, primary_key=True)

    activity_id = Column(
        "id_активности", Integer, ForeignKey("активность.id_активности")
    )

    activity = relationship("Activity")


class OtherActivity(Base):
    __tablename__ = "другое"

    id = Column("id_другого", Integer, primary_key=True)
    description = Column("описание_активности", String)

    activity_id = Column(
        "id_активности", Integer, ForeignKey("активность.id_активности")
    )

    activity = relationship("Activity")


class Meeting(Base):
    __tablename__ = "встреча"

    id = Column("id_встречи", Integer, primary_key=True)

    activity_id = Column(
        "id_активности", Integer, ForeignKey("активность.id_активности")
    )

    activity = relationship("Activity")


class Finance(Base):
    __tablename__ = "финансы"

    id = Column("id_финансовой_операции", Integer, primary_key=True)
    type = Column("тип", String)
    cost = Column("сумма", Float)
    item = Column("статья", String)
    date = Column("дата_совершения", Date)
    user_id = Column(
        "id_пользователя", Integer, ForeignKey("пользователь.id_пользователя")
    )

    user = relationship("User")
