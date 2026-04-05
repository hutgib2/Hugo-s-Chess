from settings import *
from pieces.piece import Piece

class Archer(Piece):
    def __init__(self, id, surf, color, coord, squares):
        super().__init__(surf, id, color, coord, squares)
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (2, 3)
        self.move_directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        self.move_range = 1

    def attack(self, attack_coord, round_num=0):
        self.squares[attack_coord[0]][attack_coord[1]].piece = None
