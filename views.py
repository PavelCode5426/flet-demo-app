import flet as ft

import controls as controls


class IndexPage(ft.View):
    _tabs = [controls.ReportsContainer(), controls.OrdersContainer(), controls.BillsContainer()]

    def __init__(self):
        super(IndexPage, self).__init__()
        self.container = ft.SafeArea(ft.Container())
        self.navigation_bar = controls.NavigationBar()
        self.navigation_bar.on_change = self.on_change_navigation
        self.controls = [self.container]

        self.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, shape=ft.CircleBorder())
        self.navigation_bar.selected_index = 0
        self.__set_current_selection()

    def __set_current_selection(self):
        selected = self._tabs[self.navigation_bar.selected_index]
        self.container.content = selected
        self.floating_action_button.visible = not isinstance(selected, controls.ReportsContainer)

        if isinstance(selected, controls.OrdersContainer):
            self.floating_action_button.on_click = lambda e: self.page.go('/order/create')
            self.floating_action_button.tooltip = "Nueva Orden"
        elif isinstance(selected, controls.BillsContainer):
            self.floating_action_button.on_click = lambda e: self.page.go('/bill/create')
            self.floating_action_button.tooltip = "Nuevo Gasto"

    def on_change_navigation(self, e: ft.ControlEvent):
        self.__set_current_selection()
        self.update()


class AbstractCreateOrUpdatePage(ft.View):
    create_or_update_class = None

    def __init__(self, model=None):
        super(AbstractCreateOrUpdatePage, self).__init__()
        self.model = model
        self.controls = [ft.Text(self.get_title(), style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD)),
                         self.create_or_update_class(model=model)]

    def get_title(self):
        return ""


class CreateOrUpdateOrderPage(AbstractCreateOrUpdatePage):
    create_or_update_class = controls.CreateOrUpdateOrderForm

    def get_title(self):
        return "Crear Nueva Orden" if self.model is None else "Actualizar Orden"


class CreateOrUpdateBillPage(AbstractCreateOrUpdatePage):
    create_or_update_class = controls.CreateOrUpdateBillForm

    def get_title(self):
        return "Crear Nueva Gasto" if self.model is None else "Actualizar Gasto"
