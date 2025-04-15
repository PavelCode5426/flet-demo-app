from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Float, Boolean, Text, SmallInteger, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "sqlite:///restaurant.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class CommonModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    description = Column(Text, default="")
    total = Column(Float)
    closed = Column(Boolean, default=False)


class Orden(CommonModel):
    __tablename__ = 'orden'
    number = Column(SmallInteger)
    discount = Column(Float, default=0)
    result = Column(Float)
    transference = Column(Boolean, default=False)
    comission = Column(Boolean, default=False)
    debt = Column(Boolean, default=False)
    date = Column(Date, default=datetime.now)


class Bill(CommonModel):
    __tablename__ = 'bill'
    title = Column(Text)


def create_tables():
    Base.metadata.create_all(engine)
