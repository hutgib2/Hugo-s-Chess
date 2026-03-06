from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Emperor(Piece):
    def __init(self, surf, color, squares):
        super().__init__(surf, color, squares)
        in_check = False

    def update_possible_moves(self, coordinate):
        enemy_attack_squares = []
        self.move_squares = []
        for row in range(8):
            for col in range(8):
                square = self.squares[row][col]
                if not square.piece or square.piece.color == self.color:
                    continue
                enemy_attack_squares += square.piece.attack_squares
        
        move_squares = self.get_all_moves(coordinate, 1, self.squares)
        for move in move_squares:
            if move not in enemy_attack_squares:
                self.move_squares.append(move)

    def update_attack_moves(self, start):
        self.attack_squares = []
        DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in DIRECTIONS:
            row = start[0] + direction[0]
            col = start[1] + direction[1]

            if row < 0 or row > 7 or col < 0 or col > 7:
                continue
            square = self.squares[row][col]
            if square.piece == None:
                self.attack_squares.append(square)
            elif square.piece.color != self.color:
                if type(square.piece) == Legionary:
                    if self.color == 'white' and direction == (-1, 0):
                        continue
                    elif self.color == 'black' and direction == (1, 0):
                        continue
                    elif self.has_adjacent_legionary(square, direction):
                        continue
                    
                self.attack_squares.append(square)

    def attack(self, old_coord, attack_coord, round_num=0):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None