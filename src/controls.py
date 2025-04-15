import asyncio

import flet as ft

import src.core as core


class NavigationBar(ft.NavigationBar):
    def __init__(self):
        super(NavigationBar, self).__init__(bgcolor=ft.colors.LIGHT_BLUE_ACCENT_400, destinations=[
            ft.NavigationDestination(icon=ft.icons.REPORT, label="Reporte"),
            ft.NavigationDestination(icon=ft.icons.PAYMENT, label="Ordenes"),
            ft.NavigationDestination(icon=ft.icons.NO_TRANSFER, label="Gastos"),
        ], selected_index=0)
        self.indicator_color = ft.colors.WHITE


class EmptyContent(ft.Column):
    def __init__(self, text, icon):
        super(EmptyContent, self).__init__(alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                           controls=[ft.Icon(icon, size=45), ft.Text(text, size=24)])


class CalculateSalaryForm(ft.Column):
    def __init__(self, percent):
        super(CalculateSalaryForm, self).__init__(data=percent)

        self.tips = ft.TextField(value='0', border_radius=10, keyboard_type=ft.KeyboardType.NUMBER,
                                 input_filter=ft.NumbersOnlyInputFilter(), suffix_text="CUP",
                                 on_change=self.on_change_values)
        self.workers = ft.TextField(value='1', border_radius=10, keyboard_type=ft.KeyboardType.NUMBER,
                                    input_filter=ft.NumbersOnlyInputFilter(), on_change=self.on_change_values)
        self.salary_for_workers = ft.Text("0.00", size=15)
        self.box_cash = ft.Text("0.00", size=15)

        self.controls = [
            ft.Column([
                ft.Text("Cantidad de Propinas"),
                self.tips,
                ft.Text("Cantidad de Trabajadores"),
                self.workers
            ]),
            ft.Row([ft.Text("Salario por Trabajador:", size=15), self.salary_for_workers]),
        ]

    def on_change_values(self, e: ft.ControlEvent):
        if len(self.tips.value) and len(self.workers.value):
            self.calculate_salaries()

    def calculate_salaries(self):
        workers = int(self.workers.value)
        if workers > 0:
            salary = core.calculate(self.data, float(self.tips.value), workers)
            self.salary_for_workers.value = round(salary, 2)
            self.update()

    def update_data(self, percent):
        self.data = percent
        self.calculate_salaries()


class ReportContainer(ft.Container):
    def __init__(self, title, value):
        super(ReportContainer, self).__init__(border_radius=10, bgcolor=ft.colors.GREEN_800,
                                              alignment=ft.alignment.center,
                                              padding=ft.padding.all(10))
        self.content = ft.Row([
            ft.Text(title, size=15, color=ft.colors.WHITE),
            ft.Text(f"{value} CUP", size=20, color=ft.colors.WHITE)
        ])


class IndexContainer(ft.Container):
    def __init__(self, title):
        super(IndexContainer, self).__init__()
        self.title = ft.Text(title, style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD))
        self.content = ft.Column([self.title], expand=True)


class ReportsContainer(IndexContainer):
    def __init__(self):
        super(ReportsContainer, self).__init__("Reportes")
        self.content_row = ft.Row([], wrap=True)
        self.content_form = CalculateSalaryForm(0)
        self.content.controls.append(self.content_row)
        self.content.controls.append(self.content_form)

    def render_reports(self):
        sells_info = asyncio.run(core.Reports().get_day_info())

        self.content_row.clean()
        grid_controls = self.content_row.controls
        grid_controls.append(ReportContainer("Ventas Totales:", round(sells_info.get('sells'), 2)))
        grid_controls.append(ReportContainer("Porciento:", round(sells_info.get('percent'), 2)))
        grid_controls.append(ReportContainer("Comisiones:", round(sells_info.get('comissions'), 2)))
        grid_controls.append(ReportContainer("Transferencias:", round(sells_info.get('transferences'), 2)))
        grid_controls.append(ReportContainer("Gastos:", round(sells_info.get('bills'), 2)))
        grid_controls.append(ReportContainer("Efectivo:", round(sells_info.get('efective'), 2)))

        self.content_form.update_data(sells_info.get('percent'))

    def did_mount(self):
        self.render_reports()
        self.update()


class AbstractCRUDContainer(IndexContainer):
    empty_control = EmptyContent("Sin Ordenes", ft.icons.CONTENT_COPY)
    repository: core.Repository

    def __init__(self, title, button_title):
        super(AbstractCRUDContainer, self).__init__(title)
        self.content_column = ft.Container(bgcolor=ft.colors.GREY_50, expand_loose=True, alignment=ft.alignment.center,
                                           border_radius=10)
        self.complete_button = ft.FilledTonalButton(button_title, icon=ft.icons.CHECKLIST, icon_color=ft.colors.GREEN)
        self.content.controls.append(ft.Row([self.complete_button], alignment=ft.MainAxisAlignment.END))
        self.content.controls.append(self.content_column)

    def render_empty(self):
        self.content_column.content = self.empty_control

    def render_list(self):
        pass

    def did_mount(self):
        self.content_column.clean()
        self.render_list()
        self.content_column.update()


class OrdersContainer(AbstractCRUDContainer):
    empty_control = EmptyContent("Sin Ordenes", ft.icons.CONTENT_COPY)
    repository = core.OrderRepository()

    def __init__(self):
        super(OrdersContainer, self).__init__("Ordenes", "Cerrar Ordenes")

    def on_click_edit_button_event(self, e: ft.ControlEvent):
        order = e.control.data
        self.page.go(f'/order/{order}')

    def render_list(self):
        all_orders = asyncio.run(self.repository.get_today_orders())

        if len(all_orders) == 0:
            self.render_empty()
        else:
            listview = ft.Column(spacing=20, scroll=ft.ScrollMode.ALWAYS, expand_loose=True)
            for order in all_orders:
                subtitle = ft.Row([ft.Text(f"Total: ${order.result}")])
                if order.discount > 0:
                    subtitle.controls.append(ft.Text(f"Descuento: {order.discount}%", color=ft.colors.GREEN))
                if order.comission:
                    subtitle.controls.append(ft.Text(f"USD", color=ft.colors.GREEN))
                if order.description:
                    subtitle = ft.Column([ft.Text(order.description), subtitle], spacing=2)

                if order.transference:
                    item_icon = ft.Icon(ft.icons.CREDIT_SCORE, ft.colors.ORANGE_800)
                elif order.debt:
                    item_icon = ft.Icon(ft.icons.WARNING, ft.colors.RED_ACCENT_700)
                else:
                    item_icon = ft.Icon(ft.icons.MONEY_ROUNDED, ft.colors.GREEN_900)

                order_item = ft.Dismissible(ft.ListTile(
                    title=ft.Text(f"Vale #{order.number}", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    subtitle=subtitle,
                    trailing=ft.IconButton(ft.icons.EDIT_NOTE, data=order.id, on_click=self.on_click_edit_button_event),
                    expand=True,
                    leading=item_icon
                ), dismiss_direction=ft.DismissDirection.END_TO_START,
                    on_dismiss=self.on_dismiss_list_item,
                    secondary_background=ft.Container(
                        ft.Text("Eliminar", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        alignment=ft.alignment.center_right, bgcolor=ft.colors.RED,
                        padding=ft.padding.only(right=25)))
                order_item.data = order

                listview.controls.append(order_item)
            self.content_column.content = listview

    def on_dismiss_list_item(self, e: ft.ControlEvent):
        control = e.control
        order = control.data
        asyncio.run(self.repository.delete(order))
        self.content_column.content.controls.remove(control)
        if len(self.content_column.content.controls) == 0:
            self.render_empty()
        self.content_column.update()


class BillsContainer(AbstractCRUDContainer):
    empty_control = EmptyContent("Sin Gastos", ft.icons.CONTENT_COPY)
    repository = core.BillRepository()

    def __init__(self):
        super(BillsContainer, self).__init__("Gastos", "Cerrar Gastos")

    def on_click_edit_button_event(self, e: ft.ControlEvent):
        bill = e.control.data
        self.page.go(f'/bill/{bill}')

    def render_list(self):
        all_bills = asyncio.run(self.repository.get_all())

        if len(all_bills) == 0:
            self.render_empty()
        else:
            listview = ft.Column(spacing=20, scroll=ft.ScrollMode.ALWAYS, expand_loose=True)
            for bill in all_bills:
                subtitle = ft.Row([ft.Text(f"Total: ${bill.total}")])
                if bill.description:
                    subtitle = ft.Column([ft.Text(bill.description), subtitle], spacing=2)

                bill_control = ft.Dismissible(ft.ListTile(
                    title=ft.Text(bill.title, style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                    subtitle=subtitle,
                    trailing=ft.IconButton(ft.icons.EDIT_NOTE, data=bill.id, on_click=self.on_click_edit_button_event),
                    expand=True,
                ), dismiss_direction=ft.DismissDirection.END_TO_START,
                    on_dismiss=self.on_dismiss_list_item,
                    secondary_background=ft.Container(
                        ft.Text("Eliminar", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                        alignment=ft.alignment.center_right, bgcolor=ft.colors.RED,
                        padding=ft.padding.only(right=25)))
                bill_control.data = bill

                listview.controls.append(bill_control)
            self.content_column.content = listview

    def on_dismiss_list_item(self, e: ft.ControlEvent):
        control = e.control
        bill = control.data
        asyncio.run(self.repository.delete(bill))
        self.content_column.content.controls.remove(control)
        if len(self.content_column.content.controls) == 0:
            self.render_empty()
        self.content_column.update()


class AbstractCreateOrUpdateForm(ft.Container):
    repository: core.Repository

    def __init__(self, model=None, **kwargs):
        super(AbstractCreateOrUpdateForm, self).__init__(expand=True)
        self.setup(model, **kwargs)
        self.setup_buttons(model, **kwargs)
        if model:
            self.data = model
            self.update_fields(self.data)

    def update_fields(self, value):
        pass

    def create_or_update(self, e: ft.ControlEvent):
        pass

    def setup(self, model, **kwargs):
        pass

    def setup_buttons(self, model, **kwargs):
        self.submit_button = ft.FilledButton("Agregar" if model is None else "Actualizar",
                                             on_click=self.create_or_update_event)
        self.cancel_button = ft.FilledTonalButton("Cancelar", on_click=lambda e: self.page.go("/"))

        self.buttons = ft.Row([self.submit_button, self.cancel_button], expand=True)
        self.content.controls.append(ft.Container(self.buttons, alignment=ft.alignment.center, expand=True))

    def create_or_update_event(self, e: ft.ControlEvent):
        columns = self.get_create_or_update_data()
        model = self.data
        if not model:
            instruction = self.repository.create(**columns)
        else:
            instruction = self.repository.update(model, **columns)
        asyncio.run(instruction)
        self.page.go('/')

    def get_create_or_update_data(self):
        return NotImplemented


class CreateOrUpdateOrderForm(AbstractCreateOrUpdateForm):
    repository = core.OrderRepository()

    def setup(self, model, **kwargs):
        self.order_number = ft.TextField(autofocus=True, input_filter=ft.NumbersOnlyInputFilter(),
                                         suffix_icon=ft.icons.NUMBERS_SHARP, border_radius=10)
        self.order_total = ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), suffix_text="CUP", border_radius=10)
        self.order_description = ft.TextField(multiline=True, border_radius=10)
        self.order_discount = ft.Slider(min=0, max=100, value=0, divisions=20, label="{value}%")
        self.order_transference = ft.Checkbox("Pagado con transferencia", value=False)
        self.order_debt = ft.Checkbox("El cliente con deuda", value=False)
        self.order_comission = ft.Checkbox("Carta en USD", value=False)

        self.content = ft.Column([
            ft.Text("Numero del Vale"),
            self.order_number,
            ft.Text("Total Consumido"),
            self.order_total,
            ft.Text("Descuento"),
            self.order_discount,
            ft.Text("Observaciones"),
            self.order_description,
            self.order_transference,
            self.order_debt,
            self.order_comission,
        ], expand=True)

    def update_fields(self, value):
        self.order_number.value = value.number
        self.order_total.value = value.total
        self.order_discount.value = value.discount
        self.order_transference.value = value.transference
        self.order_description.value = value.description
        self.order_debt.value = value.debt
        self.order_comission.value = value.comission

    def get_create_or_update_data(self):
        total = float(self.order_total.value)
        discount = float(self.order_discount.value)
        result = total - (total * (discount / 100))
        columns = dict(total=total, discount=discount, result=result, number=self.order_number.value,
                       closed=False, transference=self.order_transference.value, comission=self.order_comission.value,
                       description=self.order_description.value, debt=self.order_debt.value)

        return columns


class CreateOrUpdateBillForm(AbstractCreateOrUpdateForm):
    repository = core.BillRepository()

    def setup(self, model, **kwargs):
        self.bill_title = ft.TextField(autofocus=True, border_radius=10)
        self.bill_total = ft.TextField(input_filter=ft.NumbersOnlyInputFilter(), suffix_text="CUP", border_radius=10)
        self.bill_description = ft.TextField(multiline=True, border_radius=10)

        self.content = ft.Column([
            ft.Text("Titulo"),
            self.bill_title,
            ft.Text("Total"),
            self.bill_total,
            ft.Text("Descripcion"),
            self.bill_description,
        ], expand=True)

    def update_fields(self, value):
        self.bill_title.value = value.title
        self.bill_total.value = value.total
        self.bill_description.value = value.description

    def get_create_or_update_data(self):
        total = float(self.bill_total.value)
        columns = dict(total=total, closed=False, title=self.bill_title.value, description=self.bill_description.value)
        return columns
