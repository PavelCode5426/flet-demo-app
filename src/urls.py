from flet_route import path

import src.pages as pages

app_routes_with_navigation = [
    path(url="/", clear=True, view=pages.index_page),
    path(url="/order/create", clear=True, view=pages.create_or_update_order_page),
    path(url="/order/:order_id", clear=True, view=pages.create_or_update_order_page),
    path(url="/bill/create", clear=True, view=pages.create_or_update_bill_page),
    path(url="/bill/:bill_id", clear=True, view=pages.create_or_update_bill_page),
]
