import flet as ft
from janggiBoard import janggiBoard
from janggiplayer import Game
def main(page: ft.Page):
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
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
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                
            ],
            expand=True,
        )
    )

    page.add(rail)
    page.title='장기'
    page.update()
ft.app(target=main)