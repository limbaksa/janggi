import flet as ft
from flet_route import Params, Basket
import sys
sys.path.append("..")
class play_record:
    def view(self,page:ft.Page, params:Params, basket:Basket):

        def nav_change(e):
            page.go('/ai' if e.control.selected_index==1 else '/record' if e.control.selected_index==2 else '/self')
        return ft.View(
            '/record',

            controls=[
                ft.Row([
                    ft.NavigationRail(
                        selected_index=None,
                        label_type=ft.NavigationRailLabelType.ALL,
                        on_change=nav_change,
                        expand=False,
                        min_width=100,
                        min_extended_width=400,
                        group_alignment=-1,
                        destinations=[
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
                        ],
                    ),
                    ft.VerticalDivider(width=1),
                    ft.DataTable()
                ],expand=True)
            ]
        )