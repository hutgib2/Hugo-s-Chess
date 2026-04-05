from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, id, surf, color, coord, squares):
        super().__init__()
        self.id = id
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color
        self.coord = coord
        self.attack_squares = []
        self.move_squares = []
        self.squares = squares
        self.is_reloading = False
        self.is_stunned = False
        self.stunned_at = 0
        self.attacked_at = 0

    def has_adjacent_legionary(self, square, direction):
        from pieces.legionary import Legionary

        if direction == (1, -1) or direction == (-1, -1):
            row = square.coord[0]
            col = square.coord[1] + 1
            if col > 7:
                return False
        
        elif direction == (1, 1) or direction == (-1, 1):
            row = square.coord[0]
            col = square.coord[1] - 1
            if col < 0:
                return False
        else:
            return False

        defending_square = self.squares[row][col]
        if defending_square.piece and type(defending_square.piece) == Legionary and defending_square.piece.color != self.color:
            return True
        return False

    def update_possible_moves(self):
        self.move_squares = []
        for direction in self.move_directions:
            i = 1
            while i <= self.move_range:
                row = self.coord[0] + direction[0] * i
                col = self.coord[1] + direction[1] * i
                i += 1

                if row < 0 or row > 7 or col < 0 or col > 7:
                    break

                square = self.squares[row][col]
                if square.piece == None:
                    self.move_squares.append(square)
                else:
                    break

    def update_attack_moves(self):
        from pieces.emperor import Emperor
        from pieces.legionary import Legionary

        self.attack_squares = []
        for direction in self.attack_directions:
            i = self.attack_range[0]
            while i <= self.attack_range[1]:
                row = self.coord[0] + direction[0] * i
                col = self.coord[1] + direction[1] * i
                i += 1

                if row < 0 or row > 7 or col < 0 or col > 7:
                    break
                
                square = self.squares[row][col]
                if square.piece == None:
                    self.attack_squares.append(square)
                elif square.piece.color != self.color:
                    if type(square.piece) == Legionary:
                        if direction == (-1, 0) and self.color == 'white':
                            break
                        elif direction == (1, 0) and self.color == 'black':
                            break
                        elif self.has_adjacent_legionary(square, direction):
                            break
                    self.attack_squares.append(square)
                    break
                else:
                    break

    def attack(self, attack_coord, round_num=0):
        old_square = self.squares[self.coord[0]][self.coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None

    def get_state(self):
        return {
            "id": self.id,
            "coord": self.coord,
            "type": type(self).__name__,
            "color": self.color,
            "is_stunned": self.is_stunned,
            "is_reloading": self.is_reloading,
            "stunned_at": self.stunned_at,
            "attacked_at": self.attacked_at
        }

