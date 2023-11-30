import flet as ft
import janggibase
from janggiplayer import AI
import flet.canvas as cv

class janggiPiece(ft.GestureDetector):
    def __init__(self,piece:janggibase.Piece,board:"janggiBoard"):
        super().__init__()
        self.mouse_cursor=ft.MouseCursor.MOVE
        self.drag_interval=5
        self.on_pan_start=self.start_drag
        self.on_pan_update=self.drag
        self.on_pan_end=self.drop
        self.left=60*(piece.location//10)
        self.top=60*(9-piece.location%10)
        self.content=ft.Container(width=60,height=60,border_radius=ft.border_radius.all(5),content=ft.Image(f'img/{str(piece).upper()}{piece.color}.png'))
        self.board=board
        self.piece=piece
        self.slot=board.slots[piece.location]
        self.slot.ontop=self
    

    def move_on_top(self):
        self.board.controls.remove(self)
        self.board.controls.append(self)
        self.board.update()

    def bounce_back(self):
        """Returns card to its original position"""
        self.top = self.slot.top
        self.left = self.slot.left
        self.update()

    def place(self, slot):
        """Place card to the slot"""
        self.slot.ontop=None
        self.top = slot.top
        self.left = slot.left
        if slot.ontop:
            self.board.controls.remove(slot.ontop)
            self.board.piecelist.remove(slot.ontop)
            self.board.update()
        slot.ontop=self
        self.slot=slot

    def start_drag(self, e: ft.DragStartEvent):

        self.move_on_top()
        if self.piece.color==self.board.board.turn and (not self.board.ai or self.piece.color!=self.board.aiturn):
            for slot in self.board.slots:
                if self.piece.isValidMove(self.board.slots.index(slot)):
                    slot.content=ft.Image(f'img/able.png')
                    self.board.controls.remove(slot)
                    self.board.controls.append(slot)
                    slot.update()
                    self.board.update()

        self.update()

    def drag(self, e: ft.DragUpdateEvent):
        self.top = min(max(0, self.top + e.delta_y),540)
        self.left = min(max(0, self.left + e.delta_x),480)
        self.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.board.slots:
            if self.piece.isValidMove(self.board.slots.index(slot)):
                slot.content=None
                slot.update()
        for piece in self.board.piecelist:
            piece.move_on_top()
        if self.piece.color != self.board.board.turn  or (self.board.ai and self.piece.color==self.board.aiturn):
            self.bounce_back()
            self.update()
            return
        for slot in self.board.slots:
            if (abs(self.top - slot.top) < 30 and abs(self.left - slot.left) < 30):
                if self.piece.isValidMove(self.board.slots.index(slot)):
                    trymove=self.board.board.move(self.piece.location,self.board.slots.index(slot))
                    if trymove:
                        self.place(slot)
                        self.update()
                        if self.board.board.isGameOver(self.board.board.turn):
                            self.board.gameOver(self.board.board.isGameOver(self.board.board.turn))

                        if self.board.ai:
                            m=self.board.ai.getMove()
                            move=janggibase.Piece.UCIToMove(m)
                            self.board.board.move(*move)
                            piece=self.board.slots[move[0]].ontop
                            piece.place(self.board.slots[move[1]])
                            piece.update()
                            if self.board.board.isGameOver(self.board.board.turn):
                                self.board.gameOver(self.board.board.isGameOver(self.board.board.turn))

                        return
                    else:
                        self.bounce_back()
                        self.update()
                        return

        self.bounce_back()
        self.update()


class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.ontop=None
        self.width=60
        self.height=60
        self.left=left
        self.top=top
        self.opacity=0.8


class janggiBoard(ft.Stack):
    def __init__(self,board:janggibase.Board,ai=False,aiturn=None):
        super().__init__()
        cp = cv.Canvas(
                [
                    cv.Path(
                        [
                            cv.Path.MoveTo(30, 30),
                            cv.Path.LineTo(30, 570),
                            cv.Path.MoveTo(90, 30),
                            cv.Path.LineTo(90, 570),
                            cv.Path.MoveTo(150, 30),
                            cv.Path.LineTo(150, 570),
                            cv.Path.MoveTo(210, 30),
                            cv.Path.LineTo(210, 570),
                            cv.Path.MoveTo(270, 30),
                            cv.Path.LineTo(270, 570),
                            cv.Path.MoveTo(330, 30),
                            cv.Path.LineTo(330, 570),
                            cv.Path.MoveTo(390, 30),
                            cv.Path.LineTo(390, 570),
                            cv.Path.MoveTo(450, 30),
                            cv.Path.LineTo(450, 570),
                            cv.Path.MoveTo(510, 30),
                            cv.Path.LineTo(510, 570),
                            cv.Path.MoveTo(30,30),
                            cv.Path.LineTo(510,30),
                            cv.Path.MoveTo(30,90),
                            cv.Path.LineTo(510,90),
                            cv.Path.MoveTo(30,150),
                            cv.Path.LineTo(510,150),
                            cv.Path.MoveTo(30,210),
                            cv.Path.LineTo(510,210),
                            cv.Path.MoveTo(30,270),
                            cv.Path.LineTo(510,270),
                            cv.Path.MoveTo(30,330),
                            cv.Path.LineTo(510,330),
                            cv.Path.MoveTo(30,390),
                            cv.Path.LineTo(510,390),
                            cv.Path.MoveTo(30,450),
                            cv.Path.LineTo(510,450),
                            cv.Path.MoveTo(30,510),
                            cv.Path.LineTo(510,510),
                            cv.Path.MoveTo(30,570),
                            cv.Path.LineTo(510,570),
                            cv.Path.MoveTo(210,30),
                            cv.Path.LineTo(330,150),
                            cv.Path.MoveTo(330,30),
                            cv.Path.LineTo(210,150),
                            cv.Path.MoveTo(210,450),
                            cv.Path.LineTo(330,570),
                            cv.Path.MoveTo(330,450),
                            cv.Path.LineTo(210,570),

                        ],
                        paint=ft.Paint(
                            color='white',
                            stroke_width=2,
                            style=ft.PaintingStyle.STROKE,
                        ),
                    ),
                ],
                width=float("inf"),
                expand=True,
            )
        self.board=board
        self.slots=[]
        self.controls=[cp]
        self.width=540
        self.height=600
        self.ai=AI(self.board,aiturn) if ai else None
        self.aiturn=aiturn
        for i in range(90):
            self.slots.append(Slot(60*(9-i%10),60*(i//10)))
        self.controls.extend(self.slots)
        self.piecelist=[]
        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece,self))
        self.controls.extend(self.piecelist)

        
        
    def gameOver(self,result):
        dlg=ft.AlertDialog(title=ft.Text(result,size=50,color=ft.colors.GREEN if result[0]=='초' else ft.colors.RED if result[0]=='한' else ft.colors.GREY))
        dlg.open=True
        self.controls.append(dlg)
        self.update()
    
    def AI_firstmove(self):
        m=self.ai.getFirstMove()
        move=janggibase.Piece.UCIToMove(m)
        self.board.move(*move)
        piece=self.slots[move[0]].ontop
        piece.place(self.slots[move[1]])

if __name__=='__main__':
    def main(page):
        page.add(janggiBoard(janggibase.Board(15)))

    ft.app(target=main)