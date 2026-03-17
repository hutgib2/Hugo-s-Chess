from settings import *
from pieces.piece import Piece

class Emperor(Piece):
    def __init__(self, surf, color, coord, squares):
        super().__init__(surf, color, coord, squares)
        self.in_check = False
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (1, 1)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1
