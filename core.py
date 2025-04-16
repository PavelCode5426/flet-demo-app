# Repositorio base
from sqlalchemy import func

import models

worker_salary = 0
casher_salary = 200
sells_percent = 0.10
comission_percent = 0.5


def calculate(total, tips, workers):
    worker = worker_salary

    worker += (total + tips) / workers
    return worker


class Repository:
    model = None

    def __init__(self):
        self.session = models.Session()

    async def get_all(self):
        return self.session.query(self.model).all()

    async def create(self, **kwargs):
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

    async def update(self, model, **kwargs):
        for key, value in kwargs.items():
            setattr(model, key, value)
        self.session.commit()
        return model

    async def get_pk(self, pk):
        return self.session.query(self.model).filter_by(id=pk).first()

    async def delete(self, model):
        self.session.delete(model)
        self.session.commit()


class OrderRepository(Repository):
    model = models.Orden

    async def get_today_orders(self):
        return self.session.query(self.model).filter_by(closed=False).all()


class BillRepository(Repository):
    model = models.Bill


class Reports(Repository):

    def get_day_info(self):
        bills = self.session.query(func.sum(models.Bill.total).label('gastos')) \
            .filter(models.Bill.closed == False).first()

        info = self.session.query(
            func.sum(models.Orden.result).label('sells'),
            func.sum(models.Orden.result).filter(models.Orden.transference == True).label('transf'),
            func.sum(models.Orden.result).filter(models.Orden.comission == True).label('comissions'),
            func.sum(models.Orden.result).filter(models.Orden.debt == True).label('debts')
        ).filter(models.Orden.closed == False).first()

        sells = info.sells or 0
        transferences = info.transf or 0
        debts = info.debts or 0
        comissions = info.comissions * comission_percent if info.comissions is not None else 0
        percent = (sells - comissions) * sells_percent
        bills = bills.gastos

        efective = sells - percent - comissions - transferences - bills - debts

        return dict(sells=sells, transferences=transferences, comissions=comissions, percent=percent,
                    efective=efective, bills=bills)
