import asyncio

import flet as ft
from flet_route import Params, Basket

import src.core as core
import src.views as views


def index_page(page: ft.Page, params: Params, basket: Basket):
    return views.IndexPage()


def create_or_update_order_page(page: ft.Page, params: Params, basket: Basket):
    order_id = params.get('order_id')
    order = None if not order_id else asyncio.run(core.OrderRepository().get_pk(order_id))
    return views.CreateOrUpdateOrderPage(order)


def create_or_update_bill_page(page: ft.Page, params: Params, basket: Basket):
    bill_id = params.get('bill_id')
    bill = None if not bill_id else asyncio.run(core.BillRepository().get_pk(bill_id))
    return views.CreateOrUpdateBillPage(bill)
