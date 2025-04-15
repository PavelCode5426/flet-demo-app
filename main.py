import asyncio
import os.path

import flet as ft

import urls as urls
from models import create_tables
from routing import Routing


async def init():
    if os.path.isfile('restaurant.db'):
        create_tables()


def main(page: ft.Page):
    Routing(page=page, app_routes=urls.app_routes_with_navigation)
    page.go(page.route)


asyncio.run(init())
ft.app(target=main)
