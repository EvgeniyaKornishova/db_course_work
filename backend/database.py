from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

USERNAME = ""
PASSWORD = ""
DB = ""

SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@localhost/{DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
