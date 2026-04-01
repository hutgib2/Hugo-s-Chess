from settings import *
from pieces.piece import Piece


class Dragon(Piece):
    def __init__(self, surf, color, coord, squares, groups, is_stunned=False, stunned_at=0, is_reloading=False, attacked_at=0):
        super().__init__(surf, color, coord, squares, groups, is_stunned, stunned_at, is_reloading, attacked_at)
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
    #     for square in self.attack_squares:
    #         Flame(square.rect.center, self.groups)