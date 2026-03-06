from settings import *
from pieces.legionary import Piece
from pieces.legionary import Legionary

class Archer(Piece):
    def __init__(self, surf, color, squares):
        super().__init__(surf, color, squares)
        self.attack_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        self.attack_range = 3

    def update_possible_moves(self, coordinate):
        self.move_squares = self.get_all_moves(coordinate, 1, self.squares)

    def attack(self, old_coord, attack_coord, round_num=0):
        self.squares[attack_coord[0]][attack_coord[1]].piece = None
