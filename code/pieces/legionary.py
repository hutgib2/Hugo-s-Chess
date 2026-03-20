from settings import *
from pieces.piece import Piece

class Legionary(Piece):
    def __init__(self, surf, color, coord, squares, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, is_stunned, stunned_at, is_reloading, attacked_at)
        self.attack_squares = []
        self.attack_range = (1,1)
        self.move_range = 1
        if self.color == 'white':
            self.attack_directions = [(-1, 0)]
            self.move_directions = [(-1, 0)]
        elif self.color == 'black':
            self.attack_directions = [(1, 0)]
            self.move_directions = [(1, 0)]

