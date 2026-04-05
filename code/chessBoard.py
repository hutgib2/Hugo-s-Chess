from settings import *
from pieces.legionary import Legionary
from pieces.dragon import Dragon
from pieces.archer import Archer
from pieces.wizard import Wizard
from pieces.catapult import Catapult
from pieces.emperor import Emperor
from notifier import notifier

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
    def __init__(self, surf, setup_data):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (BOARD_SIZE, BOARD_SIZE))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.squares = [[], [], [], [], [], [], [], []] # creates a 2d list of Square objects
        self.pieces = {}
        self.selected_square = None
        self.turn = 'white'
        self.round_num = 0
        self.checkmate = False
        self.emperors = {
            "white": None,
            "black": None
        }
        self.gen_squares()
        self.setup_pieces(setup_data)

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

    def setup_pieces(self, setup_data):
        for piece_state in setup_data:
            piece = self.piece_from_type(piece_state)
            self.place_piece(piece.coord, piece)
            self.pieces[piece_state["id"]] = piece

    def place_piece(self, pos, piece):
        self.squares[pos[0]][pos[1]].piece = piece
        if type(piece) == Emperor:
            self.emperors[piece.color] = piece
        
    def piece_from_type(self, piece_state):
        match piece_state["type"]:
            case "Legionary":
                return Legionary(piece_state["id"], PIECE_SURFS[piece_state["color"]]['legionary'], piece_state["color"], piece_state["coord"], self.squares)
            case "Emperor":
                return Emperor(piece_state["id"], PIECE_SURFS[piece_state["color"]]['emperor'], piece_state["color"], piece_state["coord"], self.squares)
            case "Dragon":
                return Dragon(piece_state["id"], PIECE_SURFS[piece_state["color"]]['dragon'], piece_state["color"], piece_state["coord"], self.squares)
            case "Archer":
                return Archer(piece_state["id"], PIECE_SURFS[piece_state["color"]]['archer'], piece_state["color"], piece_state["coord"], self.squares)
            case "Catapult":
                return Catapult(piece_state["id"], PIECE_SURFS[piece_state["color"]]['catapult'], piece_state["color"], piece_state["coord"], self.squares)
            case "Wizard":
                return Wizard(piece_state["id"], PIECE_SURFS[piece_state["color"]]['wizard'], piece_state["color"], piece_state["coord"], self.squares)

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
        
        # clear board
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                square.piece = None

        # place pieces
        for piece_state in snapshot["pieces"]:
            piece = self.pieces[piece_state['id']]
            piece.coord = piece_state['coord']
            piece.is_stunned = piece_state['is_stunned']
            piece.stunned_at = piece_state['stunned_at']
            piece.is_reloading = piece_state['is_reloading']
            piece.attacked_at = piece_state['attacked_at']
            self.place_piece(piece_state["coord"], piece)
            
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

    def update_moves(self, square):
        square.piece.update_possible_moves()
        allowed_moves = self.filter_invalid_moves(square)

        square.piece.update_attack_moves()
        allowed_attacks = self.filter_invalid_attacks(square)

        if type(square.piece) == Wizard:
            square.piece.update_swap_moves()
            allowed_swaps = self.filter_invalid_swaps(square)
            square.piece.swap_squares = allowed_swaps

        square.piece.move_squares = allowed_moves
        square.piece.attack_squares = allowed_attacks

    def filter_invalid_moves(self, square):
        updated_moves = []
        for move_square in square.piece.move_squares:
            self.move_piece(square, move_square)
            if not self.in_check():
                updated_moves.append(move_square)
            self.move_piece(move_square, square)
        return updated_moves

    def filter_invalid_swaps(self, square):
        updated_moves = []
        for swap_square in square.piece.swap_squares:
            self.swap_piece(square, swap_square)
            if not self.in_check():
                updated_moves.append(swap_square)
            self.swap_piece(swap_square, square)
        return updated_moves

    def filter_invalid_attacks(self, square):
        updated_moves = []
        for attack_square in square.piece.attack_squares:
            snapshot = self.take_snapshot()
            self.attack_piece(square, attack_square)
            if not self.in_check():
                updated_moves.append(attack_square)
            
            self.apply_snapshot(snapshot)
        return updated_moves
    
    def in_check(self):
        emperor = self.emperors[self.turn]
        emperor_coord = emperor.coord
                
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color == self.turn:
                    continue
                square.piece.update_attack_moves()
                for attack_square in square.piece.attack_squares:
                    if attack_square.coord == emperor_coord:
                        return True
        return False
    
    def evaluate_check_mate(self):
        all_moves = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color != self.turn:
                    continue
                self.update_moves(square)
                all_moves.extend(square.piece.move_squares)
                all_moves.extend(square.piece.attack_squares)
                if type(square.piece) == Wizard:
                    all_moves.extend(square.piece.swap_squares)

        if len(all_moves) == 0:
            notifier.notify('Checkmate!')
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

        if self.in_check():
            print('in check')
            self.evaluate_check_mate()