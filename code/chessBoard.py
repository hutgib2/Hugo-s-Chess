from settings import *
from enum import Enum
from textSprite import TextSprite
from pieces.legionary import Legionary
from pieces.dragon import Dragon
from pieces.archer import Archer
from pieces.wizard import Wizard
from pieces.catapult import Catapult
from pieces.emperor import Emperor
import copy
import pprint

class Square():
    def __init__(self, rect, coord):
        self.rect = rect # represents the area of the square
        self.coord = coord
        self.piece = None # whether and which piece is on that square
        self.is_possible_move = False
        self.is_selected = False
        self.is_attack_move = False
        self.is_swappable = False

class ChessBoard(pygame.sprite.Sprite):
    def __init__(self, surf):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (BOARD_SIZE, BOARD_SIZE))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.squares = [[], [], [], [], [], [], [], []] # creates a 2d list of Square objects
        self.selected_square = None
        self.turn = 'white'
        self.round_num = 0
        self.emperors = {
            "white": None,
            "black": None
        }
        self.gen_squares()
        self.checkmate = False

        # images
        self.select_indicator = pygame.transform.smoothscale(BOARD_SURFS['select_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.move_indicator = pygame.transform.smoothscale(BOARD_SURFS['move_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.attack_indicator = pygame.transform.smoothscale(BOARD_SURFS['attack_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.stun_indicator = pygame.transform.smoothscale(BOARD_SURFS['stun_indicator'], (TILE_WIDTH / 1.1, TILE_WIDTH / 1.1))
        self.switch_indicator = pygame.transform.smoothscale(BOARD_SURFS['switch_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.reload_indicator = pygame.transform.smoothscale(BOARD_SURFS['reload_indicator'], (TILE_WIDTH / 2, TILE_WIDTH / 2))
        self.move_indicator.set_alpha(200)
        self.attack_indicator.set_alpha(200)
        self.stun_indicator.set_alpha(240)

    # creates a 2d list of rects representing the individual squares on the board
    def gen_squares(self):
        self.squares = [[], [], [], [], [], [], [], []]
        pos_x, pos_y = self.rect.topleft # starting the rows and columns from the top left

        for row in range(8):
            for col in range(8): 
                square_rect = pygame.Rect(pos_x + (col * TILE_WIDTH), pos_y, TILE_WIDTH, TILE_WIDTH) # creates a rect that specifies the area of a square
                self.squares[row].append(Square(square_rect, (row,col))) # it appends the whole area of a square and gives that square a piece
            pos_y += TILE_WIDTH # shifts to the next row

    def place_piece(self, pos, piece):
        self.squares[pos[0]][pos[1]].piece = piece
        if type(piece) == Emperor:
            self.emperors[piece.color] = piece

    def take_snapshot(self):
        snapshot = {
            "round_num": self.round_num,
            "turn": self.turn,
            "pieces": [],
        }
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if square.piece:
                    snapshot["pieces"].append(square.piece.get_state())
        return snapshot

    def apply_snapshot(self, snapshot):
        self.round_num = snapshot["round_num"]
        self.turn = snapshot["turn"]
        
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                square.piece = None

        for piece in snapshot["pieces"]:
            self.place_piece(piece["coord"], self.piece_from_type(piece))

    def piece_from_type(self, piece):
        match piece["type"]:
            case "Legionary":
                return Legionary(PIECE_SURFS[piece["color"]]['legionary'], piece["color"], piece["coord"], self.squares, piece["is_stunned"], piece["stunned_at"], piece["is_reloading"], piece["attacked_at"])
            case "Emperor":
                return Emperor(PIECE_SURFS[piece["color"]]['emperor'], piece["color"], piece["coord"], self.squares, piece["is_stunned"], piece["stunned_at"], piece["is_reloading"], piece["attacked_at"])
            case "Dragon":
                return Dragon(PIECE_SURFS[piece["color"]]['dragon'], piece["color"], piece["coord"], self.squares, piece["is_stunned"], piece["stunned_at"], piece["is_reloading"], piece["attacked_at"])
            case "Archer":
                return Archer(PIECE_SURFS[piece["color"]]['archer'], piece["color"], piece["coord"], self.squares,  piece["is_stunned"], piece["stunned_at"], piece["is_reloading"], piece["attacked_at"])
            case "Catapult":
                return Catapult(PIECE_SURFS[piece["color"]]['catapult'], piece["color"], piece["coord"], self.squares, piece["is_stunned"], piece["stunned_at"], piece["is_reloading"], piece["attacked_at"])
            case "Wizard":
                return Wizard(PIECE_SURFS[piece["color"]]['wizard'], piece["color"], piece["coord"], self.squares, piece["is_stunned"], piece["stunned_at"], piece["is_reloading"], piece["attacked_at"])

    def select_piece(self, click_square):
        if self.selected_square:
            self.selected_square.is_selected = False
        click_square.is_selected = True
        self.update_moves(click_square)
        self.selected_square = click_square

    def deselect_piece(self):
        if self.selected_square:
            self.selected_square.is_selected = False
            self.selected_square = None
                
    def update_moves(self, click_square):
        click_square.piece.update_possible_moves()
        # print(f'all moves = {len(click_square.piece.move_squares)}')
        allowed_moves = self.filter_check_moves(click_square, click_square.piece.move_squares, 'move')

        click_square.piece.update_attack_moves()
        allowed_attacks = self.filter_check_moves(click_square, click_square.piece.attack_squares, 'attack')

        if type(click_square.piece) == Wizard:
            click_square.piece.update_swap_moves()
            allowed_swaps = self.filter_check_moves(click_square, click_square.piece.swap_squares, 'swap')
            click_square.piece.swap_squares = allowed_swaps

        click_square.piece.move_squares = allowed_moves
        # print(f'allowed moves = {len(click_square.piece.move_squares)}')
        click_square.piece.attack_squares = allowed_attacks
    
    def filter_check_moves(self, click_square, moves, move_type):
        updated_moves = []
        for move in moves:
            # save board state
            snapshot = self.take_snapshot()
            color = click_square.piece.color
            in_check = self.emperors[color].in_check

            match move_type:
                case 'move':
                    self.move_piece(click_square, move)
                case 'attack':
                    self.attack_piece(click_square, move)
                case 'swap':
                    self.swap_piece(click_square, move)
            
            if not self.in_check(color):
                updated_moves.append(move)
            
            # revert board state
            self.apply_snapshot(snapshot)
            self.emperors[color].in_check = in_check
        return updated_moves

    def update_enemy_attack_squares(self, color):
        all_enemy_attack_squares = []
        for row in range(8):
            for col in range(8): # for each square on the board, update their attack moves only if there's an opoonent's piece on that square
                square = self.squares[row][col]
                if square.piece and square.piece.color != color:
                    square.piece.update_attack_moves()
                    all_enemy_attack_squares.extend(square.piece.attack_squares)
        
        for square in all_enemy_attack_squares:
            if square.coord == self.emperors[color].coord:
                self.emperors[color].in_check = True

    def move_piece(self, old_square, new_square):
        new_square.piece = old_square.piece
        old_square.piece = None
        new_square.piece.coord = new_square.coord

    def swap_piece(self, old_square, new_square):
        temp = old_square.piece
        old_square.piece = new_square.piece
        new_square.piece = temp
        old_square.piece.coord = old_square.coord
        new_square.piece.coord = new_square.coord

    def attack_piece(self, old_square, attack_square):
        old_square.piece.attack(attack_square.coord, self.round_num)
        if not old_square.piece:
            attack_square.piece.coord = attack_square.coord
        if type(old_square.piece) == Catapult:
            old_square.piece.is_reloading = True
            old_square.piece.attacked_at = self.round_num


    def in_check(self, color):
        self.update_enemy_attack_squares(color)
        if self.emperors[color].in_check:
            return True
        return False

    def in_check_mate(self, color):
        # if possible moves for one side is 0 and emperor's in check
        # it's a draw if no can make a move and they're not in check
        count = 0
        all_moves = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece:
                    continue
                if square.piece.color != color:
                    continue
                all_moves.extend(square.piece.move_squares)
                
                all_moves.extend(square.piece.attack_squares)
                
                if type(square.piece) == Wizard:
                    all_moves.extend(square.piece.swap_squares)
                count+=1

        # print(f'all moves = {all_moves}')
        # print(f'piece count = {count}')
        if len(all_moves) == 0 and self.in_check(color):
            self.checkmate = True

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
                if square.piece and square.piece.is_stunned == True:
                    pygame.display.get_surface().blit(self.stun_indicator, square.rect)
                if square.is_attack_move == True:
                    pygame.display.get_surface().blit(self.attack_indicator, square.rect)
                if square.is_swappable == True:
                    pygame.display.get_surface().blit(self.switch_indicator, square.rect)
                if square.piece and square.piece.is_reloading == True:
                    pygame.display.get_surface().blit(self.reload_indicator, square.rect)

    def update(self):
        # print(f'begin updated(): {self.selected_square.piece.move_squares}')

        # this resets every squares state
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                square.is_possible_move = False
                square.is_attack_move = False
                square.is_swappable = False
                if square.piece:
                    if square.piece.is_stunned and self.round_num - square.piece.stunned_at > 2:
                        square.piece.is_stunned = False
                    if square.piece.is_reloading and self.round_num - square.piece.attacked_at > 3:
                        square.piece.is_reloading = False
                
        # print(f'after reset(): {self.selected_square.piece.move_squares}')
        if self.selected_square and self.selected_square.piece:
            for square in self.selected_square.piece.move_squares:
                square.is_possible_move = True
            if not self.selected_square.piece.is_reloading:
                for square in self.selected_square.piece.attack_squares:
                    if square.piece != None:
                        square.is_attack_move = True
            
            if type(self.selected_square.piece) == Wizard:
                for square in self.selected_square.piece.swap_squares:
                    square.is_swappable = True

        # these for loops promote legionary to archer 
        for square in self.squares[0]:
            if square.piece and square.piece.color == 'white' and type(square.piece) == Legionary:
                square.piece = Archer(PIECE_SURFS['white']['archer'], 'white', square.coord, self.squares)
        for square in self.squares[7]:
            if square.piece and square.piece.color == 'black' and type(square.piece) == Legionary:
                square.piece = Archer(PIECE_SURFS['black']['archer'], 'black', square.coord, self.squares)

        self.in_check_mate(self.turn)
        # print(f'end updated(): {self.selected_square.piece.move_squares}')