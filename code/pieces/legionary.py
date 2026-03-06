from settings import *

class Piece(pygame.sprite.Sprite):
    def __init__(self, surf, color, squares):
        super().__init__()
        self.image = pygame.transform.smoothscale(surf, (TILE_WIDTH, TILE_WIDTH))
        self.color = color
        self.attack_squares = self.update_attack_moves
        self.move_squares = []
        self.squares = squares
        self.is_stunned = False
        self.stunned_at = None
        self.can_attack = True
        self.attacked_at = 0

    def has_adjacent_legionary(self, square, direction):
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

    def get_all_moves(self, start, range, squares):
        move_squares = []
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in DIRECTIONS:
            i = 1
            while i <= range:
                row = start[0] + direction[0] * i
                col = start[1] + direction[1] * i
                i += 1

                if row < 0 or row > 7 or col < 0 or col > 7:
                    break
                
                if squares[row][col].piece != None:
                    break
                
                move_squares.append(squares[row][col])
        return move_squares

    def update_attack_moves(self, start):
        self.attack_squares = []
        for direction in self.attack_directions:
            i = 1
            while i <= self.attack_range:
                row = start[0] + direction[0] * i
                col = start[1] + direction[1] * i
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


class Legionary(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        self.attack_squares = []
        self.attack_range = 1
        if self.color == 'white':
            self.attack_directions = [(-1, 0)]
        elif self.color == 'black':
            self.attack_directions = [(1, 0)]


    def update_possible_moves(self, coordinate):
        self.move_squares = []
        row, col = coordinate # extracts row and col from the coordinate

        if self.color == 'white' and row > 0:
            front_square = self.squares[row-1][col]
        elif self.color == 'black' and row < 7:
            front_square = self.squares[row+1][col]
        else:
            front_square = None
        
        if front_square and front_square.piece == None:
            self.move_squares.append(front_square)

    def attack(self, old_coord, attack_coord, round_num=0):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None

