import flet as ft
import janggibase
from janggiplayer import AI
import flet.canvas as cv
from db import db

class janggiPiece(ft.GestureDetector):
    def __init__(self,piece:janggibase.Piece,board:"janggiBoard"):
        super().__init__()
        self.mouse_cursor=ft.MouseCursor.BASIC
        self.drag_interval=5
        self.on_pan_start=None
        self.on_pan_update=None
        self.on_pan_end=None
        self.left=60*(piece.location//10)
        self.top=60*(9-piece.location%10)
        self.content=ft.Container(width=60,height=60,border_radius=ft.border_radius.all(5),content=ft.Image(f'img/{str(piece).upper()}{piece.color}.png'))
        self.board=board
        self.piece=piece
        self.slot=board.slots[piece.location]
        self.slot.ontop=self
        self.visible=True

    def place(self, slot):
        self.slot.ontop=None
        self.top = slot.top
        self.left = slot.left
        if slot.ontop:
            self.board.controls.remove(slot.ontop)
            self.board.piecelist.remove(slot.ontop)
        self.board.update()
        slot.ontop=self
        self.slot=slot


class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.ontop=None
        self.width=60
        self.height=60
        self.left=left
        self.top=top
        self.opacity=0.8


class replayBoard(ft.Stack):
    def __init__(self,variant,record):
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
        self.gameRecord=record.split()
        self.variant=variant
        self.board=janggibase.Board(self.variant)
        self.fenRecord=[self.board.makeFEN()]
        self.slots=[]
        self.controls=[cp]
        self.width=540
        self.height=600
        self.move_num=0
        for i in range(90):
            self.slots.append(Slot(60*(9-i%10),60*(i//10)))
        self.controls.extend(self.slots)
        self.piecelist=[]
        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece,self))
        self.controls.extend(self.piecelist)
        self.moveNotation=[]

        for i in range(len(self.gameRecord)-1):
            movingPiece=''
            if self.gameRecord[i]=='@@@@':
                move=[0,0]
            else:
                move=[int(self.gameRecord[i][:2]),int(self.gameRecord[i][2:])]
                movingPiece=self.board.boardState[move[0]]
            if isinstance(movingPiece,janggibase.Cannon):
                movingPiece='포'
            elif isinstance(movingPiece,janggibase.Chariot):
                movingPiece='차'
            elif isinstance(movingPiece,janggibase.Elephant):
                movingPiece='상'
            elif isinstance(movingPiece,janggibase.Guard):
                movingPiece='사'
            elif isinstance(movingPiece,janggibase.Horse):
                movingPiece='마'
            elif isinstance(movingPiece,janggibase.King):
                movingPiece='궁'
            elif isinstance(movingPiece,janggibase.Soldier):
                if movingPiece.color:
                    movingPiece='병'
                else:
                    movingPiece='졸'
            else:
                movingPiece=''
            notation=janggibase.Piece.moveToNotation(*move)
            self.moveNotation.append(notation[:2]+movingPiece+notation[2:])
            self.board.move(*move)
            self.fenRecord.append(self.board.makeFEN())
        self.board=janggibase.Board(self.variant)

    def reset(self,board:janggibase.Board):
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
        self.controls=[cp]
        self.slots=[]
        for i in range(90):
            self.slots.append(Slot(60*(9-i%10),60*(i//10)))
        self.controls.extend(self.slots)
        self.piecelist=[]

        for color in range(2):
            for piece in self.board.pieces[color]:
                self.piecelist.append(janggiPiece(piece,self))
        self.controls.extend(self.piecelist)



    def move(self,e):
        if self.move_num<len(self.gameRecord)-1:
            self.move_num+=1
            self.board=janggibase.Board(self.variant,self.fenRecord[self.move_num])
            self.reset(self.board)
            self.update()

    def undo_move(self,e):
        if self.move_num:
            self.move_num-=1
            self.board=janggibase.Board(self.variant,self.fenRecord[self.move_num])
            self.reset(self.board)
            self.update()
    
    def set_move(self,move_num):
        self.move_num=move_num+1
        self.board=janggibase.Board(self.variant,self.fenRecord[self.move_num])
        self.reset(self.board)
        self.update()


if __name__=='__main__':
    def main(page):
        page.add(replayBoard(janggibase.Board(15)))

    ft.app(target=main)