import flet as ft
class Sidebar(ft.UserControl):
 
    def __init__(self,app_layout, page):
        super().__init__()
        self.app_layout = app_layout
        self.page = page
        self.top_nav_items = [
            ft.NavigationRailDestination(
                icon=ft.icons.PLAY_ARROW, 
                selected_icon=ft.icons.PLAY_ARROW_OUTLINED, 
                label="혼자 두기"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.ADB),
                selected_icon_content=ft.Icon(ft.icons.ADB_OUTLINED),
                label="AI와 두기",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LIST,
                selected_icon_content=ft.Icon(ft.icons.LIST_OUTLINED),
                label_content=ft.Text("대국 목록 보기"),
            )
 
        ]
        self.top_nav_rail=ft.NavigationRail(
            selected_index=None,
            label_type=ft.NavigationRailLabelType.ALL,
            on_change=self.top_nav_change,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            group_alignment=-1,
            destinations=self.top_nav_items,
            
            expand=True
        )
        
 
    def build(self):
        self.view = ft.Container(
            content=ft.Column([
                self.top_nav_rail,
                # divider
                ft.Container(
                    bgcolor=ft.colors.BLACK26,
                    border_radius=ft.border_radius.all(30),
                    height=1,
                    alignment=ft.alignment.center_right,
                    width=220
                ),
            ], tight=True),
            padding=ft.padding.all(15),
            margin=ft.margin.all(0),
            width=150,
            bgcolor=ft.colors.BLUE_GREY,
        )
        return self.view
 
    def top_nav_change(self, e):
        self.top_nav_rail.selected_index = e.control.selected_index
        self.update()
        self.page.update()