import flet as ft
from flet_route import Params, Basket

def start_view(page,params,basket):
    return ft.View('/',
                   [ft.Text('장기'),
                    ft.ElevatedButton("혼자 두기",on_click=lambda _:page.go('/self')),
                    ft.ElevatedButton("AI와 두기",on_click=lambda _:page.go('/ai')),
                    ft.ElevatedButton("대국 기록 보기",on_click=lambda _:page.go('/record')),
                    ])