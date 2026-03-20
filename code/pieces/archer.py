from settings import *
from pieces.piece import Piece

class Archer(Piece):
    def __init__(self, surf, color, coord, squares, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, is_stunned, stunned_at, is_reloading, attacked_at)
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (2, 3)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1

    def attack(self, old_coord, attack_coord, round_num=0):
        self.squares[attack_coord[0]][attack_coord[1]].piece = None
