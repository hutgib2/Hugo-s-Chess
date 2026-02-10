from settings import *
from enum import Enum
from textSprite import TextSprite
from piece import *
from pieces.legionary import Legionary
from pieces.dragon import Dragon
from pieces.archer import Archer
from pieces.wizard import Wizard
from pieces.catapult import Catapult
from pieces.emperor import Emperor

class Square():
    def __init__(self, rect, coordinate):
        self.rect = rect # represents the area of the square
        self.coord = coordinate
        self.piece = None # whether and which piece is on that square
        self.is_possible_move = False
        self.is_selected = False
        self.is_kill_move = False

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (BOARD_SIZE, BOARD_SIZE))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.squares = [[], [], [], [], [], [], [], []] # creates a 2d list of Square objects
        self.gen_squares()
        self.setup_pieces()
        self.selected_square = None
        self.possible_moves = []
        self.kill_moves = []
        self.yellow_square = pygame.transform.smoothscale(BOARD_SURFS['select'], (TILE_WIDTH, TILE_WIDTH))
        self.move_indicator = pygame.transform.smoothscale(BOARD_SURFS['move_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.kill_indicator = pygame.transform.smoothscale(BOARD_SURFS['kill'], (TILE_WIDTH, TILE_WIDTH))

    # creates a 2d list of rects representing the individual squares on the board
    def gen_squares(self):
        pos_x, pos_y = self.rect.topleft # starting the rows and columns from the top left

        for row in range(8):
            for col in range(8): 
                square_rect = pygame.Rect(pos_x + (col * TILE_WIDTH), pos_y, TILE_WIDTH, TILE_WIDTH) # creates a rect that specifies the area of a square
                self.squares[row].append(Square(square_rect, (row,col))) # it appends the whole area of a square and gives that square a piece
            pos_y += TILE_WIDTH # shifts to the next row

    def setup_pieces(self):
        for col in range(8):
            self.place_piece((6, col), Legionary(WHITE_SURFS['legionary'], 'white', self.squares))
        for col in range(8):
            self.place_piece((1, col), Legionary(BLACK_SURFS['legionary'], 'black', self.squares))

        self.place_piece((7, 5), Wizard(WHITE_SURFS['wizard'], 'white', self.squares))
        self.place_piece((7, 2), Wizard(WHITE_SURFS['wizard'], 'white', self.squares))
        self.place_piece((0, 5), Wizard(BLACK_SURFS['wizard'], 'black', self.squares))
        self.place_piece((0, 2), Wizard(BLACK_SURFS['wizard'], 'black', self.squares))

        self.place_piece((7, 0), Catapult(WHITE_SURFS['catapult'], 'white', self.squares))
        self.place_piece((7, 7), Catapult(WHITE_SURFS['catapult'], 'white', self.squares))
        self.place_piece((0, 0), Catapult(BLACK_SURFS['catapult'], 'black', self.squares))
        self.place_piece((0, 7), Catapult(BLACK_SURFS['catapult'], 'black', self.squares))

        self.place_piece((7, 4), Emperor(WHITE_SURFS['emperor'], 'white', self.squares))
        self.place_piece((0, 4), Emperor(BLACK_SURFS['emperor'], 'black', self.squares))

        self.place_piece((7, 3), Archer(WHITE_SURFS['archer'], 'white', self.squares))
        self.place_piece((0, 3), Archer(BLACK_SURFS['archer'], 'black', self.squares))

        self.place_piece((7, 6), Dragon(WHITE_SURFS['dragon'], 'white', self.squares))
        self.place_piece((7, 1), Dragon(WHITE_SURFS['dragon'], 'white', self.squares))
        self.place_piece((0, 6), Dragon(BLACK_SURFS['dragon'], 'black', self.squares))
        self.place_piece((0, 1), Dragon(BLACK_SURFS['dragon'], 'black', self.squares))

    def place_piece(self, pos, piece):
        self.squares[pos[0]][pos[1]].piece = piece
        
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
                if square.is_possible_move == True:
                    pygame.display.get_surface().blit(self.move_indicator, square.rect)
                if square.is_selected == True:
                    pygame.display.get_surface().blit(self.yellow_square, square.rect)
                if square.piece != None:
                    pygame.display.get_surface().blit(square.piece.image, square.rect)
                if square.is_kill_move == True:
                    pygame.display.get_surface().blit(self.kill_indicator, square.rect)

    def update(self):
        # this resets the possible move squares
        for move in self.possible_moves:
            square = self.squares[move[0]][move[1]]
            square.is_possible_move = False

        for move in self.kill_moves:
            square = self.squares[move[0]][move[1]]
            square.is_kill_move = False   


        if self.selected_square != None:
            self.possible_moves = self.selected_square.piece.possible_moves(self.selected_square.coord)
            for move in self.possible_moves:
                move_square = self.squares[move[0]][move[1]]
                move_square.is_possible_move = True

            self.kill_moves = self.selected_square.piece.kill_moves(self.selected_square.coord)
            for move in self.kill_moves:
                move_square = self.squares[move[0]][move[1]]
                move_square.is_kill_move = True
            
        
