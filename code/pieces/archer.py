from settings import *
from pieces.piece import Piece

class Archer(Piece):
    def __init__(self, id, color, coord, squares):
        super().__init__(id, 'archer', color, coord, squares)
        self.type = "archer"
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (2, 3)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1

    def attack(self, attack_coord, round_num=0):
        attack_square = self.squares[attack_coord[0]][attack_coord[1]]
        score = PIECE_SCORES[attack_square.piece.type]
        attack_square.piece = None
        return score