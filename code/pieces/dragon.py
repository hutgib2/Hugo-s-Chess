from settings import *
from pieces.piece import Piece


class Dragon(Piece):
    def __init__(self, id, surf, color, coord, squares):
        super().__init__(id, surf, color, coord, squares)
        self.attack_range = (1,1)
        if self.color == 'white':
            self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1)]
        elif self.color == 'black':
            self.attack_directions = [(1, -1), (1, 0), (1, 1), (0, 1), (0, -1)]
        
        self.move_directions = [(1, -2), (1, 2), (-1, 2), (-1, -2,), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        self.move_range = 1

    def attack(self, attack_coord, round_num=0):
        for square in self.attack_squares:
            square.piece = None
    
    # def animate_attack(self, _):
    