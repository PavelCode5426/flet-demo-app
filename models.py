from datetime import datetime

from peewee import *

db = SqliteDatabase('restaurant.db')


class ComonModel(Model):
    id = IntegerField(primary_key=True)
    description = TextField(default="")
    total = FloatField()
    closed = BooleanField(default=False)

    class Meta:
        abstract = True
        database = db


class Orden(ComonModel):
    number = SmallIntegerField()
    discount = FloatField(default=0)
    result = FloatField()
    transference = BooleanField(default=False)
    comission = BooleanField(default=False)
    debt = BooleanField(default=False)
    date = DateField(default=datetime.now)


class Bill(ComonModel):
    title = TextField()


def create_tables():
    with db:
        db.create_tables([Orden, Bill])
