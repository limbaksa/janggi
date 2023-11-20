import flet as ft
from sidebar import Sidebar
 
class AppLayout(ft.Row):
    def __init__(
        self,
        app,
        page: ft.Page,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.page = page
        self.toggle_nav_rail_button = ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_LEFT, icon_color=ft.colors.BLUE_GREY_400, selected=False,
            selected_icon=ft.icons.ARROW_CIRCLE_RIGHT, on_click=self.toggle_nav_rail)
        self.sidebar = Sidebar(self, page)
        self._active_view: ft.Control = ft.Column(controls=[
            ft.Text("Active View")
        ], alignment="center", horizontal_alignment="center")
        self.controls = [self.sidebar,
                         self.toggle_nav_rail_button, self.active_view]
 
    @property
    def active_view(self):
        return self._active_view
 
    @active_view.setter
    def active_view(self, view):
        self._active_view = view
        self.update()
 