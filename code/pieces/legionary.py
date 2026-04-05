from settings import *
from pieces.piece import Piece

class Legionary(Piece):
    def __init__(self, id, surf, color, coord, squares):
        super().__init__(surf, id, color, coord, squares)
        self.attack_squares = []
        self.attack_range = (1,1)
        self.move_range = 1
        if self.color == 'white':
            self.attack_directions = [(-1, 0)]
            self.move_directions = [(-1, 0)]
        elif self.color == 'black':
            self.attack_directions = [(1, 0)]
            self.move_directions = [(1, 0)]

