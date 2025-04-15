import models as models

worker_salary = 0
casher_salary = 200
sells_percent = 0.10
comission_percent = 0.5


def calculate(total, tips, workers):
    worker = worker_salary

    worker += (total + tips) / workers
    return worker


class Repository:
    _instances = None
    model = None

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances = instance
        return cls._instances[cls]

    async def get_all(self):
        return self.model.select()

    async def create(self, *args, **kwargs):
        return self.model.create(*args, **kwargs)

    async def update(self, model, **kwargs):
        model.update_from_dict(kwargs)
        return model.save()

    async def get_pk(self, pk):
        return self.model.get(pk=pk)

    async def delete(self, model):
        return model.delete_instance()


class OrderRepository(Repository):
    model = models.Orden

    async def get_today_orders(self):
        return self.model.select().filter(closed=False)


class BillRepository(Repository):
    model = models.Bill


class Reports(Repository):

    async def get_day_info(self):
        return dict()
        # info = await models.Orden.filter(closed=False).annotate(
        #     sells=tortoise.functions.Sum('result'),
        #     transf=tortoise.functions.Sum('result', _filter=tortoise.models.Q(transference=True)),
        #     comissions=tortoise.functions.Sum('result', _filter=tortoise.models.Q(comission=True)),
        #     debts=tortoise.functions.Sum('result', _filter=tortoise.models.Q(debt=True)),
        # ).first()
        #
        # sells = info.sells if info.sells is not None else 0
        # debts = info.debts if info.debts is not None else 0
        # transferences = info.transf if info.transf is not None else 0
        # comissions = info.comissions * comission_percent if info.comissions is not None else 0
        # percent = (sells - comissions) * sells_percent
        # bills = await models.Bill.exclude(closed=True).annotate(gastos=tortoise.functions.Sum('total')).first()
        # bills = bills.gastos
        #
        # efective = sells - percent - comissions - transferences - bills - debts
        # return dict(sells=sells, transferences=transferences, comissions=comissions, percent=percent,
        #             efective=efective, bills=bills)
