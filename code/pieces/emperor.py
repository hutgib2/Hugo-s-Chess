from settings import *
from pieces.piece import Piece

class Emperor(Piece):
    def __init__(self, surf, color, coord, squares, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, is_stunned, stunned_at, is_reloading, attacked_at)
        self.in_check = False
        self.attack_directions = [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]
        self.attack_range = (1, 1)
        self.move_directions = [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]
        self.move_range = 1
