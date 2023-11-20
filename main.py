import flet as ft
from janggiBoard import janggiBoard
from janggiplayer import Game
from sidebar import Sidebar
from app_layout import AppLayout
def main(page: ft.Page):
    
    page.add(
        ft.Row(
            [
                #rail,
                ft.VerticalDivider(width=1),
                
            ],
            expand=True,
        )
    )
    #print(rail.top_nav_rail.selected_index)

    page.title='장기'
    page.update()
ft.app(target=main)