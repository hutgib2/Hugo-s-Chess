from settings import *
from support import *
from textSprite import TextSprite
from timer import Timer
from chessBoard import ChessBoard

class Chess2026():
    def __init__(self):
        self.running = True
        self.board = ChessBoard(BOARD_SURFS['chess_board'])

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for row in range(8):
                        for col in range(8):
                            square = self.board.squares[row][col]
                            if square.rect.collidepoint(event.pos) and square.is_possible_move == True:
                                square.piece = self.board.selected_square.piece
                                self.board.selected_square.piece = None
                            if square.rect.collidepoint(event.pos) and square.piece != None:
                                self.board.selected_square = square
                                square.is_selected = True
                            else:
                                square.is_selected = False

            self.board.update()             
            screen.fill('bisque')
            self.board.render()
            pygame.display.update()

game = Chess2026()
game.run()
pygame.quit()