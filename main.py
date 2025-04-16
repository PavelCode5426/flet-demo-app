import os.path

import flet as ft

import urls as urls
from logger import logger
from models import create_tables
from routing import Routing


def init_database():
    if not os.path.isfile('restaurant.db'):
        create_tables()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    Routing(page=page, app_routes=urls.app_routes_with_navigation)
    page.go(page.route)


try:
    logger.info("Inicializando base de datos")
    init_database()
    logger.info("Base de datos inicializada")
    ft.app(target=main)
except Exception as e:
    logger.critical(e)
