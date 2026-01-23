from settings import *
from support import *
from textSprite import TextSprite
from timer import Timer
from chessBoard import ChessBoard
from legionary import Legionary

class Chess2026():
    def __init__(self):
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.board = ChessBoard(SURFS['chess_board'], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), WINDOW_WIDTH / 3, self.all_sprites)
        self.pieces = pygame.sprite.Group()
        self.setup_pieces()
        self.selected_square = pygame.transform.smoothscale(SURFS['yellow_square'], (self.board.tile_width, self.board.tile_width))
        self.selected_pos = None

    def setup_pieces(self):
        for col in range(8):
            Legionary(SURFS['legionary_white'], self.board.coordinates[6][col].center, self.board.tile_width, (self.pieces, self.all_sprites))
        for col in range(8):
            Legionary(SURFS['legionary_black'], self.board.coordinates[1][col].center, self.board.tile_width, (self.pieces, self.all_sprites))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for piece in self.pieces:
                        if piece.rect.collidepoint(event.pos):
                            self.selected_pos = piece.rect.topleft

            screen.fill('bisque')
            self.all_sprites.update()
            if self.selected_pos != None:
                screen.blit(self.selected_square, self.selected_pos)
            pygame.display.update()

game = Chess2026()
game.run()
pygame.quit()