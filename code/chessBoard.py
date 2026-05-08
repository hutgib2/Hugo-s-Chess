from settings import *
from pieces.legionary import Legionary
from pieces.dragon import Dragon
from pieces.archer import Archer
from pieces.wizard import Wizard
from pieces.catapult import Catapult
from pieces.emperor import Emperor
from button import InteractiveButton

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
    def __init__(self, surf, setup_data, players, notifier):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (BOARD_SIZE, BOARD_SIZE))
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.squares = [[], [], [], [], [], [], [], []] # creates a 2d list of Square objects
        self.players = players
        self.pieces = {}
        self.all_pieces = pygame.sprite.Group()
        self.selected_square = None
        self.game_over = False
        self.game_blocked = False
        self.gen_squares()
        self.create_pieces(setup_data['pieces'])
        self.apply_snapshot(setup_data)
        self.notifier = notifier

        self.promotion_sprites = pygame.sprite.Group()

        # images
        self.select_indicator = pygame.transform.smoothscale(BOARD_SURFS['select_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.move_indicator = pygame.transform.smoothscale(BOARD_SURFS['move_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.attack_indicator = pygame.transform.smoothscale(BOARD_SURFS['attack_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.stun_indicator = pygame.transform.smoothscale(BOARD_SURFS['stun_indicator'], (TILE_WIDTH / 1.2, TILE_WIDTH / 1.2))
        self.switch_indicator = pygame.transform.smoothscale(BOARD_SURFS['switch_indicator'], (TILE_WIDTH, TILE_WIDTH))
        self.reload_indicator = pygame.transform.smoothscale(BOARD_SURFS['reload_indicator'], (TILE_WIDTH / 2, TILE_WIDTH / 2))
        self.move_indicator.set_alpha(200)
        self.attack_indicator.set_alpha(200)
        self.stun_indicator.set_alpha(240)
        self.switch_indicator.set_alpha(200)

    @property
    def enemy_color(self):
        return 'white' if self.turn == 'black' else 'black'

    # creates a 2d list of rects representing the individual squares on the board
    def gen_squares(self):
        self.squares = [[], [], [], [], [], [], [], []]
        pos_x, pos_y = self.rect.topleft # starting the rows and columns from the top left

        for row in range(8):
            for col in range(8): 
                square_rect = pygame.Rect(pos_x + (col * TILE_WIDTH), pos_y, TILE_WIDTH, TILE_WIDTH) # creates a rect that specifies the area of a square
                self.squares[row].append(Square(square_rect, (row,col))) # it appends the whole area of a square and gives that square a piece
            pos_y += TILE_WIDTH # shifts to the next row

    def create_pieces(self, piece_data):
        for piece_state in piece_data:
            piece = self.piece_from_type(piece_state)
            self.pieces[piece_state["id"]] = piece
            # self.place_piece(piece.coord, piece)
            # self.all_pieces.add(piece)

    def place_piece(self, pos, piece):
        square = self.squares[pos[0]][pos[1]]
        square.piece = piece
        if type(piece) == Emperor:
            self.players[piece.color].emperor = piece
        
    def piece_from_type(self, piece_state):
        match piece_state["type"]:
            case "legionary":
                return Legionary(piece_state["id"], piece_state["color"], piece_state["coord"], self.squares)
            case "emperor":
                return Emperor(piece_state["id"], piece_state["color"], piece_state["coord"], self.squares)
            case "dragon":
                return Dragon(piece_state["id"], piece_state["color"], piece_state["coord"], self.squares)
            case "archer":
                return Archer(piece_state["id"], piece_state["color"], piece_state["coord"], self.squares)
            case "catapult":
                return Catapult(piece_state["id"], piece_state["color"], piece_state["coord"], self.squares)
            case "wizard":
                return Wizard(piece_state["id"], piece_state["color"], piece_state["coord"], self.squares)
            case _:
                print(f'Unknown type {piece_state["type"]}')

    def take_snapshot(self):
        snapshot = {
            "round_num": self.round_num,
            "turn": self.turn,
            "pieces": [],
            "scores": {
                'white': self.players['white'].score,
                'black': self.players['black'].score,
            }
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
        self.players['white'].set_score(snapshot["scores"]['white'])
        self.players['black'].set_score(snapshot["scores"]['black'])
        
        # clear board
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if square.piece:
                    square.piece.remove_piece()

        self.apply_piece_state(snapshot['pieces'])

    def apply_piece_state(self,  piece_state):
        # place pieces
        for piece_state in piece_state:
            piece = self.pieces[piece_state['id']]
            piece.set_position(tuple(piece_state['coord']))
            piece.is_stunned = piece_state['is_stunned']
            piece.stunned_at = piece_state['stunned_at']
            piece.is_reloading = piece_state['is_reloading']
            piece.attacked_at = piece_state['attacked_at']
            piece.has_moved = piece_state['has_moved']
            if piece.type == 'emperor' and piece.has_moved:
                piece.update_range()
            self.place_piece(piece.coord, piece)
            self.all_pieces.add(piece)

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
        new_square.piece.set_position(new_square.coord)

    def swap_piece(self, old_square, new_square):
        temp = old_square.piece
        old_square.piece = new_square.piece
        new_square.piece = temp
        old_square.piece.set_position(old_square.coord)
        new_square.piece.set_position(new_square.coord)

    def attack_piece(self, old_square, attack_square):
        killed_pieces = old_square.piece.attack(attack_square.coord, self.round_num)
        # if not old_square.piece:
        #     attack_square.piece.coord = attack_square.coord
        if type(old_square.piece) == Catapult:
            old_square.piece.is_reloading = True
            old_square.piece.attacked_at = self.round_num
        return killed_pieces

    def update_moves(self, square):
        if not square or not square.piece:
            return
        square.piece.update_attack_moves()
        self.filter_invalid_attacks(square)
        
        square.piece.update_possible_moves()
        self.filter_invalid_moves(square)

        if type(square.piece) == Wizard:
            square.piece.update_swap_moves()
            self.filter_invalid_swaps(square)

    def filter_invalid_moves(self, square):
        allowed_moves = []
        color = square.piece.color
        for move_square in square.piece.move_squares:
            self.move_piece(square, move_square)
            if not self.in_check(color):
                allowed_moves.append(move_square)
            self.move_piece(move_square, square)
        square.piece.move_squares = allowed_moves

    def filter_invalid_swaps(self, square):
        allowed_moves = []
        color = square.piece.color
        for swap_square in square.piece.swap_squares:
            self.swap_piece(square, swap_square)
            if not self.in_check(color):
                allowed_moves.append(swap_square)
            self.swap_piece(swap_square, square)
        square.piece.swap_squares = allowed_moves

    def filter_invalid_attacks(self, square):
        allowed_moves = []
        color = square.piece.color
        snapshot = self.take_snapshot()
        for attack_square in square.piece.attack_squares:
            if not attack_square.piece or attack_square.piece.color == color:
                continue
            self.attack_piece(square, attack_square)
            if not self.in_check(color):
                allowed_moves.append(attack_square)
            self.apply_snapshot(snapshot)
        square.piece.attack_squares = allowed_moves

    def in_check(self, color):
        enemy_color = 'white' if color == 'black' else 'black'
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color != enemy_color:
                    continue
                square.piece.update_attack_moves()
                for attack_square in square.piece.attack_squares:
                    if attack_square.coord == self.players[color].emperor.coord:
                        return True
        return False
    
    def has_possible_moves(self, color):
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color != color:
                    continue
                self.update_moves(square)
                if len(square.piece.move_squares) > 0 or len(square.piece.attack_squares) > 0:
                    return True
                if type(square.piece) == Wizard and len(square.piece.swap_squares) > 0:
                    return True
        return False
    
    def increment_promotion_select(self, color):
        self.selected = self.selected + 1 if self.selected < len(self.promotion_options) - 1 else 0
        self.selected_promotion = self.promotion_options[self.selected]
        self.promotion_button.set_image(PIECE_SURFS[color][self.selected_promotion])

    def decrement_promotion_select(self, color):
        self.selected = self.selected - 1 if self.selected > 0 else len(self.promotion_options) - 1
        self.selected_promotion = self.promotion_options[self.selected]
        self.promotion_button.set_image(PIECE_SURFS[color][self.selected_promotion])

    def offer_promotion(self, square):
        self.game_blocked = True
        self.promotion_options = ['archer', 'catapult', 'dragon', 'wizard']
        self.selected = 0
        self.selected_promotion = self.promotion_options[self.selected]
        color = square.piece.color
        self.promotion_pos = self.rect.topleft + pygame.Vector2(-TILE_WIDTH, TILE_WIDTH) if color == 'white' else self.rect.bottomright + pygame.Vector2(TILE_WIDTH, -TILE_WIDTH)
        self.promotion_button = InteractiveButton(PIECE_SURFS[color][self.selected_promotion], self.promotion_pos, (TILE_WIDTH, TILE_WIDTH), self.promotion_sprites, lambda: self.promote_piece(square, color, self.selected_promotion), '')
        InteractiveButton(BOARD_SURFS['chevron'], self.promotion_button.rect.midbottom + pygame.Vector2(TILE_WIDTH/6, TILE_WIDTH/4), (TILE_WIDTH/4, TILE_WIDTH/3), self.promotion_sprites, lambda: self.increment_promotion_select(color), '')
        InteractiveButton(pygame.transform.flip(BOARD_SURFS['chevron'], True, False), self.promotion_button.rect.midbottom + pygame.Vector2(-TILE_WIDTH/6, TILE_WIDTH/4), (TILE_WIDTH/4, TILE_WIDTH/3), self.promotion_sprites, lambda: self.decrement_promotion_select(square.piece.color), '')


    def promote_piece(self, square, color, piece_type):
        # piece_id = len(self.pieces)
        piece_id = square.piece.id
        square.piece.kill()
        square.piece = self.piece_from_type({
            'id': piece_id,
            'type': piece_type,
            'color': color,
            'coord': square.coord,
        })
        self.all_pieces.add(square.piece)
        self.pieces[piece_id] = square.piece
        self.promotion_sprites.empty()
        self.game_blocked = False

    def check_promotion(self):
        for square in self.squares[0]:
            if square.piece and square.piece.color == 'white' and type(square.piece) == Legionary:
                return square
        for square in self.squares[7]:
            if square.piece and square.piece.color == 'black' and type(square.piece) == Legionary:
                return square
        return None


    def render(self):
        pygame.display.get_surface().blit(self.image, self.rect) # draws chessboard
        self.promotion_sprites.update()
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

    def evaluate_checkmate(self, color):
        in_check = self.in_check(color)
        has_moves = self.has_possible_moves(color)

        if in_check and has_moves:
            self.notifier.notify('Check!')
        elif in_check and not has_moves:
            self.notifier.notify('Checkmate!')
            self.game_over = True
        elif not in_check and not has_moves:
            self.notifier.notify('Draw!')
            self.game_over = True
               
    def update_after_round(self):
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if square.piece:
                    if square.piece.is_stunned and self.round_num - square.piece.stunned_at > 1:
                        square.piece.is_stunned = False
                    if square.piece.is_reloading and self.round_num - square.piece.attacked_at > 1:
                        square.piece.is_reloading = False

        # Promote legionary to archer if at back row
        promotion_square = self.check_promotion()
        if promotion_square:
            self.offer_promotion(promotion_square)

        self.deselect_piece()
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.round_num += 1
        self.evaluate_checkmate('black')
        self.evaluate_checkmate('white')

    def update(self):
        # this resets every squares state
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                square.is_possible_move = False
                square.is_attack_move = False
                square.is_swappable = False

        # update selected squares move options
        if self.selected_square and self.selected_square.piece:
            for square in self.selected_square.piece.move_squares:
                square.is_possible_move = True
            if not self.selected_square.piece.is_reloading:
                for square in self.selected_square.piece.attack_squares:
                    if square.piece != None:
                        square.is_attack_move = True
            
            if self.selected_square.piece.type == 'wizard':
                for square in self.selected_square.piece.swap_squares:
                    square.is_swappable = True
