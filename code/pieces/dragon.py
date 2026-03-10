from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Dragon(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        self.attack_range = 1
        if self.color == 'white':
            self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
        elif self.color == 'black':
            self.attack_directions = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1)]
        
        self.move_directions = [(1, -2), (1, 2), (-1, 2), (-1, -2,), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        self.move_range = 1

    def attack(self, old_coord, attack_coord, round_num=0):
        for square in self.attack_squares:
            square.piece = None