import flet as ft
from flet_route import Routing, path
from views.main_view import main_view
from views.self_play import self_play
from views.ai_play import ai_play
from views.play_record import play_record

def main(page: ft.Page):
    self=self_play()
    ai=ai_play()
    record=play_record()

    app_routes=[
        path(url='/',clear=True,view=main_view),
        path(url='/self',clear=True,view=self.view),
        path(url='/ai',clear=True,view=ai.view),
        path(url='/record',clear=True,view=record.view)
    ]
    
    Routing(page=page,app_routes=app_routes)

    page.title='장기'
    page.go(page.route)
    page.update()
ft.app(target=main)