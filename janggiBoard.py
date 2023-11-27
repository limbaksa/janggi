import flet as ft
import janggibase


class janggiPiece(ft.GestureDetector):
    def __init__(self,piece):
        super().__init__()
        self.mouse_cursor=ft.MouseCursor.MOVE
        self.drag_interval=5
        self.on_pan_update=self.drag
        self.left=0
        self.top=0
        self.content=ft.Container(width=70,height=70,border_radius=ft.border_radius.all(6),content=ft.Image(f'img/{str(piece).upper()}{piece.color}.png'))
    
    def drag(self,e: ft.DragUpdateEvent):
       e.control.top = max(0, e.control.top + e.delta_y)
       e.control.left = max(0, e.control.left + e.delta_x)
       e.control.update()



class janggiBoard(ft.UserControl):
    def __init__(self,board:janggibase.Board):
        super().__init__()
        self.board=board


    def build(self):
        #self.game.AImove()
        def drag(e: ft.DragUpdateEvent):
            e.control.top = max(0, e.control.top + e.delta_y)
            e.control.left = max(0, e.control.left + e.delta_x)
            e.control.update()
        piecelist=[]
        for color in range(2):
            for piece in self.board.pieces[color]:
                piecelist.append(janggiPiece(piece))
        
        
        return piecelist

if __name__=='__main__':
    def main(page):
        page.add(janggiBoard(janggibase.Board(15)))

    ft.app(target=main)