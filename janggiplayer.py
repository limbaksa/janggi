import janggibase
import subprocess
import time
class Player:
    def __init__(self,board:janggibase.Board,color:int):
        self.board=board
        self.color=color
    
    def getMove(self)->str:
        return ''

class User(Player):
    def getMove(self)->str:
        return input()

class AI(Player):
    def __init__(self, board: janggibase.Board, color: int):
        super().__init__(board, color)
        l=['eh','he']
        L=['EH','HE']
        self.process= subprocess.Popen('stockfish', stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        self.process.stdin.write('xboard\n')
        self.process.stdin.write('protover 2\n')
        self.process.stdin.write('option EvalFile=janggi-4d3de2fee245.nnue\n')
        self.process.stdin.write('option Use NNUE=1\n')
        self.process.stdin.write('option VariantPath=variants.ini\n')
        self.process.stdin.flush()
        self.process.stdin.write('new\n')
        self.process.stdin.write(f'variant janggi_{l[self.board.variant&1]+l[(self.board.variant&2)>>1]+L[(self.board.variant&4)>>2]+L[(self.board.variant&8)>>3]}\n')
        self.process.stdin.flush()
    
    def getMove(self)->str:
        self.process.stdin.write(f'setboard {self.board.makeFEN()}\n')
        self.process.stdin.write('go\n')
        self.process.stdin.flush()
        time.sleep(2)
        self.process.stdin.write('?\n')
        self.process.stdin.flush()
        while True:
            line=self.process.stdout.readline()
            if line.startswith('move'):
                print(line)
                return line.split()[1]
            
class Game:
    def __init__(self,variant:int,player1:str,player2:str):
        self.board:janggibase.Board=janggibase.Board(variant)
        self.players:list=[]
        if player1=='User':
            self.players.append(User(self.board,0))
        else:
            self.players.append(AI(self.board,0))
        
        if player2=='User':
            self.players.append(User(self.board,1))
        else:
            self.players.append(AI(self.board,1))

if __name__=='__main__':
    g=Game(5,'AI','AI')
    while True:
        m=g.players[g.board.turn].getMove()
        move=janggibase.Piece.UCIToMove(m)
        g.board.move(*move)
        print('-'*50)
        g.board.showBoard()
        print('-'*50)
