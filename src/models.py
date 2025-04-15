from tortoise import fields
from tortoise.models import Model
from tortoise.timezone import now


class ComonModel(Model):
    id = fields.IntField(primary_key=True)
    description = fields.TextField(default="")
    total = fields.FloatField()
    closed = fields.BooleanField(default=False)

    class Meta:
        abstract = True


class Orden(ComonModel):
    number = fields.SmallIntField()
    discount = fields.FloatField(default=0)
    result = fields.FloatField()
    transference = fields.BooleanField(default=False)
    comission = fields.BooleanField(default=False)
    debt = fields.BooleanField(default=False)
    date = fields.DateField(default=now)


class Bill(ComonModel):
    title = fields.TextField()
