from settings import *
from support import *
from textSprite import TextSprite
from timer import Timer
from chessBoard import ChessBoard

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
                            click_square = self.board.squares[row][col]
                            if not click_square.rect.collidepoint(event.pos):
                                continue
                            if click_square.is_swappable:
                                self.board.swap_piece(self.board.selected_square, click_square)
                                self.switch_turn()
                            elif click_square.piece and click_square.piece.color == self.turn and not click_square.piece.is_stunned:
                                if self.board.selected_square:
                                    self.board.selected_square.is_selected = False
                                self.board.selected_square = click_square
                                click_square.is_selected = True
                            elif click_square.is_possible_move:
                                self.board.move_piece(self.board.selected_square, click_square)
                                self.switch_turn()
                            elif click_square.is_attack_move:
                                self.board.attack_piece(self.board.selected_square, click_square, self.round_num)
                                self.switch_turn()
                            elif click_square.piece == None and self.board.selected_square:
                                self.board.selected_square.is_selected = False
                                self.board.selected_square = None


            self.board.update(self.round_num)
            screen.fill('bisque')
            self.board.render()
            pygame.display.update()

game = Chess2026()
game.run()
pygame.quit()