from settings import *
from pieces.piece import Piece

class Emperor(Piece):
    def __init__(self, id, color, coord, squares):
        super().__init__(id, 'emperor', color, coord, squares)
        self.type = "emperor"
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = (1, 1)
        self.move_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.move_range = 1
