from settings import *
from support import *
from textSprite import TextSprite
from timer import Timer
from chessBoard import ChessBoard

def move_piece(old_square, new_square):
    new_square.piece = old_square.piece
    old_square.piece = None

def swap_piece(old_square, new_square):
    temp = old_square.piece
    old_square.piece = new_square.piece
    new_square.piece = temp

def attack_piece(old_square, attack_square, round_num):
    old_square.piece.attack(old_square.coord, attack_square.coord, round_num)

class Chess2026():
    def __init__(self):
        self.running = True
        self.board = ChessBoard(BOARD_SURFS['chess_board'])
        self.turn = 'white'
        self.round_num = 0

    def switch_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
        self.board.selected_square.is_selected = False
        self.board.selected_square = None
        self.round_num += 1

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for row in range(8):
                        for col in range(8):
                            square = self.board.squares[row][col]
                            if not square.rect.collidepoint(event.pos):
                                continue
                            if square.piece and square.piece.color == self.turn and not square.piece.is_stunned:
                                if self.board.selected_square:
                                    self.board.selected_square.is_selected = False
                                self.board.selected_square = square
                                square.is_selected = True
                            if square.is_possible_move:
                                move_piece(self.board.selected_square, square)
                                self.switch_turn()
                            if square.is_attack_move:
                                attack_piece(self.board.selected_square, square, self.round_num)
                                self.switch_turn()
                            if square.is_swappable:
                                swap_piece(self.board.selected_square, square)
                                self.switch_turn()

            self.board.update(self.round_num)
            screen.fill('bisque')
            self.board.render()
            pygame.display.update()

game = Chess2026()
game.run()
pygame.quit()