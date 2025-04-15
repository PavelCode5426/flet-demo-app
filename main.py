import flet as ft
from tortoise import Tortoise, run_async

import urls as urls
from routing import Routing


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        _create_db=True,
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


def main(page: ft.Page):
    Routing(page=page, app_routes=urls.app_routes_with_navigation)
    page.go(page.route)


run_async(init())
ft.app(target=main)
