class Products(Base):
    id = Column("id_товара", Integer, primary_key=True)
    name = Column("наименование", String)
    price = Column("стоимость", Float)
    amount = Column("количество", Integer)
    deadline = Column("срочность_покупки", Date)
    approved = Column("подтвержден", String)
    shop_list_id = Column("id_списка_покупок", Integer)
