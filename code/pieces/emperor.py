from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Emperor(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        in_check = False
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = 1

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

    def attack(self, old_coord, attack_coord, round_num=0):
        old_square = self.squares[old_coord[0]][old_coord[1]]
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        attack_square.piece = old_square.piece
        old_square.piece = None