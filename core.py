# Repositorio base
import models


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
