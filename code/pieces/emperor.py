from settings import *
from pieces.piece import Piece

class Emperor(Piece):
    def __init__(self, surf, color, coord, squares, groups, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, groups, is_stunned, stunned_at, is_reloading, attacked_at)
        self.in_check = False
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (1, 1)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1
