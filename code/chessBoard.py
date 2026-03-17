from settings import *
from enum import Enum
from textSprite import TextSprite
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
        self.is_attack_move = False
        self.is_swappable = False
        self.is_reloading = False
        self.is_stunned = False
        self.stunned_at = None
        self.attacked_at = 0

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (BOARD_SIZE, BOARD_SIZE))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.squares = [[], [], [], [], [], [], [], []] # creates a 2d list of Square objects
        self.gen_squares()
        self.setup_pieces()
        self.selected_square = None
        
        # images
        self.select_indicator = pygame.transform.smoothscale(BOARD_SURFS['select_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.move_indicator = pygame.transform.smoothscale(BOARD_SURFS['move_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.attack_indicator = pygame.transform.smoothscale(BOARD_SURFS['attack_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.stun_indicator = pygame.transform.smoothscale(BOARD_SURFS['stun_indicator'], (TILE_WIDTH / 2, TILE_WIDTH / 2))
        self.switch_indicator = pygame.transform.smoothscale(BOARD_SURFS['switch_indicator'], (TILE_WIDTH / 2, TILE_WIDTH / 2))
        self.reload_indicator = pygame.transform.smoothscale(BOARD_SURFS['reload_indicator'], (TILE_WIDTH / 2, TILE_WIDTH / 2))
        self.move_indicator.set_alpha(200)
        self.attack_indicator.set_alpha(200)
        self.stun_indicator.set_alpha(240)
        self.switch_indicator.set_alpha(200)

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
            self.place_piece((6, col), Legionary(WHITE_SURFS['legionary'], 'white', (6, col), self.squares))
        for col in range(8):
            self.place_piece((1, col), Legionary(BLACK_SURFS['legionary'], 'black', (1, col), self.squares))

        self.place_piece((7, 5), Wizard(WHITE_SURFS['wizard'], 'white', (7, 5), self.squares))
        self.place_piece((7, 2), Wizard(WHITE_SURFS['wizard'], 'white', (7, 2), self.squares))
        self.place_piece((0, 5), Wizard(BLACK_SURFS['wizard'], 'black', (0, 5), self.squares))
        self.place_piece((0, 2), Wizard(BLACK_SURFS['wizard'], 'black', (0, 2), self.squares))

        self.place_piece((7, 0), Catapult(WHITE_SURFS['catapult'], 'white', (7, 0), self.squares))
        self.place_piece((7, 7), Catapult(WHITE_SURFS['catapult'], 'white', (7, 7), self.squares))
        self.place_piece((0, 0), Catapult(BLACK_SURFS['catapult'], 'black', (0, 0), self.squares))
        self.place_piece((0, 7), Catapult(BLACK_SURFS['catapult'], 'black', (0, 7), self.squares))

        self.emperors = {
            "white": Emperor(WHITE_SURFS['emperor'], 'white', (7, 4), self.squares),
            "black": Emperor(BLACK_SURFS['emperor'], 'black', (0, 4), self.squares)
        }
        self.place_piece((7, 4), self.emperors["white"])
        self.place_piece((0, 4), self.emperors["black"])

        self.place_piece((7, 3), Archer(WHITE_SURFS['archer'], 'white', (7, 3), self.squares))
        self.place_piece((0, 3), Archer(BLACK_SURFS['archer'], 'black', (0, 3), self.squares))

        self.place_piece((7, 6), Dragon(WHITE_SURFS['dragon'], 'white', (7, 6), self.squares))
        self.place_piece((7, 1), Dragon(WHITE_SURFS['dragon'], 'white', (7, 1), self.squares))
        self.place_piece((0, 6), Dragon(BLACK_SURFS['dragon'], 'black', (0, 6), self.squares))
        self.place_piece((0, 1), Dragon(BLACK_SURFS['dragon'], 'black', (0, 1), self.squares))

    def place_piece(self, pos, piece):
        self.squares[pos[0]][pos[1]].piece = piece

    def select_piece(self, click_square):
        if self.selected_square:
            self.selected_square.is_selected = False
        click_square.is_selected = True
        click_square.piece.update_possible_moves(click_square.coord)
        self.remove_check_moves(click_square)
        self.selected_square = click_square

    def update_enemy_attack_squares(self, color):
        for row in range(8):
            for col in range(8): # for each square on the board, update their attack moves only if there's an opoonent's piece on that square
                square = self.squares[row][col]
                if square.piece and square.piece.color != color:
                    square.piece.update_attack_moves(square.coord)
                
    def remove_check_moves(self, click_square):
        updated_moves = []
        for move_square in click_square.piece.move_squares:
            color = click_square.piece.color
            self.move_piece(click_square, move_square)
            self.update_enemy_attack_squares(color)
            # if emperor is in check, don't append to updated moves. else append then move piece back.
            if self.emperors[color].in_check == False:
                updated_moves.append(move_square)
            self.move_piece(move_square, click_square)
            self.emperors[color].in_check = False
        click_square.piece.move_squares = updated_moves
    
    def move_piece(self, old_square, new_square):
        new_square.piece = old_square.piece
        old_square.piece = None
        if old_square.is_reloading == True:
            old_square.is_reloading = False
            new_square.is_reloading = True
            new_square.attacked_at = old_square.attacked_at
            old_square.attacked_at = 0
            new_square.piece.coord = new_square.coord

    def swap_piece(self, old_square, new_square):
        temp = old_square.piece
        old_square.piece = new_square.piece
        new_square.piece = temp
        old_square.piece.coord = old_square.coord
        new_square.piece.coord = new_square.coord

    def attack_piece(self, old_square, attack_square, round_num):
        old_square.piece.attack(old_square.coord, attack_square.coord, round_num)
        if not old_square.piece:
            attack_square.piece.coord = attack_square.coord
        if type(old_square.piece) == Catapult:
            old_square.is_reloading = True
            old_square.attacked_at = round_num

    def render(self):
        pygame.display.get_surface().blit(self.image, self.rect) # draws chessboard
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if square.is_possible_move == True:
                    pygame.display.get_surface().blit(self.move_indicator, square.rect)
                if square.is_selected == True:
                    pygame.display.get_surface().blit(self.select_indicator, square.rect)
                if square.piece != None:
                    pygame.display.get_surface().blit(square.piece.image, square.rect)
                if square.piece and square.is_stunned == True:
                    pygame.display.get_surface().blit(self.stun_indicator, square.rect)
                if square.is_attack_move == True:
                    pygame.display.get_surface().blit(self.attack_indicator, square.rect)
                if square.is_swappable == True:
                    pygame.display.get_surface().blit(self.switch_indicator, square.rect)
                if square.is_reloading == True:
                    pygame.display.get_surface().blit(self.reload_indicator, square.rect)

    def update(self, round_num):
        # this resets squares
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                square.is_possible_move = False
                square.is_attack_move = False
                square.is_swappable = False
                if square.is_stunned and round_num - square.stunned_at > 2:
                    square.is_stunned = False
                if square.is_reloading and round_num - square.attacked_at > 3:
                    square.is_reloading = False
                if square.piece:
                    square.piece.update_attack_moves(square.coord)

        if self.selected_square and self.selected_square.piece:
            for square in self.selected_square.piece.move_squares:
                square.is_possible_move = True
            if not self.selected_square.is_reloading:
                for square in self.selected_square.piece.attack_squares:
                    if square.piece != None:
                        square.is_attack_move = True
            
            if type(self.selected_square.piece) == Wizard:
                self.selected_square.piece.update_swap_moves(self.selected_square.coord)
                
        for square in self.squares[0]:
            if square.piece and square.piece.color == 'white' and type(square.piece) == Legionary:
                square.piece = Archer(WHITE_SURFS['archer'], 'white', square.coord, self.squares)
        for square in self.squares[7]:
            if square.piece and square.piece.color == 'black' and type(square.piece) == Legionary:
                square.piece = Archer(BLACK_SURFS['archer'], 'black', square.coord, self.squares)
