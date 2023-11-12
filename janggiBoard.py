import flet as ft
from janggiplayer import Game

class janggiBoard(ft.UserControl):
    def __init__(self,game:Game):
        super().__init__()
        self.game=game

    def build(self):
        return ft.Text(self.game.board.makeFEN())