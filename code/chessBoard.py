from settings import *
from enum import Enum
from textSprite import TextSprite
from piece import Piece

class Square():
    def __init__(self, rect):
        self.rect = rect # represents the area of the square
        self.piece = None # whether and which piece is on that square

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self, surf, pos, width):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (width, width))
        self.rect = self.image.get_frect(center=pos)
        self.width = width
        self.tile_width = self.width / 8
        self.gen_squares()
        self.setup_pieces()
        self.selected_square = pygame.transform.smoothscale(square_surf, (self.tile_width, self.tile_width))

    # creates a 2d list of rects representing the individual squares on the board
    def gen_squares(self):
        self.squares = [[], [], [], [], [], [], [], []] # creates a 2d list of Square objects
        pos_x, pos_y = self.rect.topleft # starting the rows and columns from the top left

        for row in range(8):
            for col in range(8): 
                square_rect = pygame.Rect(pos_x + (col * self.tile_width), pos_y, self.tile_width, self.tile_width) # creates a rect that specifies the area of a square
                self.squares[row].append(Square(square_rect)) # it appends the whole area of a square and gives that square a piece
            pos_y += self.tile_width # shifts to the next row

    def setup_pieces(self):
        for col in range(8):
            self.squares[6][col].piece = Piece(WHITE_SURFS['legionary'], self.tile_width)
        for col in range(8):
            self.squares[1][col].piece = Piece(BLACK_SURFS['legionary'], self.tile_width)

        self.squares[7][2].piece = Piece(WHITE_SURFS['wizard'], self.tile_width)
        self.squares[7][5].piece = Piece(WHITE_SURFS['wizard'], self.tile_width)
        self.squares[0][2].piece = Piece(BLACK_SURFS['wizard'], self.tile_width)
        self.squares[0][5].piece = Piece(BLACK_SURFS['wizard'], self.tile_width)

        self.squares[7][0].piece = Piece(WHITE_SURFS['catapult'], self.tile_width)
        self.squares[7][7].piece = Piece(WHITE_SURFS['catapult'], self.tile_width)
        self.squares[0][0].piece = Piece(BLACK_SURFS['catapult'], self.tile_width)
        self.squares[0][7].piece = Piece(BLACK_SURFS['catapult'], self.tile_width)

        self.squares[7][4].piece = Piece(WHITE_SURFS['emperor'], self.tile_width)
        self.squares[0][4].piece = Piece(BLACK_SURFS['emperor'], self.tile_width)

    def test_coordinates(self):
        for row in range(8):
            for col in range(8):
                square = self.coordinates[row][col]
                coordinate = f'({row}, {col})'
                TextSprite(coordinate, square.center, 'black', 50, self.groups)

    def render(self):
        pygame.display.get_surface().blit(self.image, self.rect) # draws chessboard
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if square.piece != None:
                    if square.piece.is_selected == True:
                        pygame.display.get_surface().blit(self.selected_square, square.rect)
                    pygame.display.get_surface().blit(square.piece.image, square.rect)
                